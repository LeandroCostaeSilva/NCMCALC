from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
import logging

from app import app, db
from models import User, Calculation, TaxDetail, CostDetail, ProductScenario
from forms import LoginForm, RegisterForm, ProductForm, CostForm, ProfitabilityForm, ScenarioForm, ForgotPasswordForm, ResetPasswordForm
from services.tax_calculator import BrazilianTaxCalculator
from services.currency_service import CurrencyService
from services.ncm_service import NCMService

# Initialize services
tax_calculator = BrazilianTaxCalculator()
currency_service = CurrencyService()
ncm_service = NCMService()

@app.route('/')
def index():
    """Página inicial"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal do usuário"""
    # Estatísticas do usuário
    total_calculations = Calculation.query.filter_by(user_id=current_user.id).count()
    recent_calculations = Calculation.query.filter_by(user_id=current_user.id)\
                                         .order_by(Calculation.created_at.desc())\
                                         .limit(5).all()
    saved_scenarios = ProductScenario.query.filter_by(user_id=current_user.id).count()
    
    return render_template('dashboard.html', 
                         total_calculations=total_calculations,
                         recent_calculations=recent_calculations,
                         saved_scenarios=saved_scenarios)

# Rotas de Autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login do usuário"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('E-mail ou senha incorretos.', 'danger')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de novo usuário"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Verificar se email já existe
        if User.query.filter_by(email=form.email.data).first():
            flash('E-mail já cadastrado. Faça login.', 'warning')
            return redirect(url_for('login'))
        
        # Criar novo usuário
        user = User(
            email=form.email.data,
            name=form.name.data,
            company=form.company.data,
            user_type=form.user_type.data
        )
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar conta. Tente novamente.', 'danger')
            logging.error(f"Erro ao criar usuário: {str(e)}")
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('index'))

# Rotas de Recuperação de Senha
@app.route('/esqueci-senha', methods=['GET', 'POST'])
def forgot_password():
    """Página de solicitação de recuperação de senha"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Gerar token de recuperação
            token = user.generate_reset_token()
            db.session.commit()
            
            # Simular envio de email (sem SMTP real por enquanto)
            # Em produção, aqui enviaria um email real
            reset_url = url_for('reset_password', token=token, _external=True)
            
            # Para desenvolvimento, vamos mostrar o link na mensagem
            flash(f'Link de recuperação: {reset_url}', 'info')
            flash('Instruções de recuperação foram enviadas para seu email.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email não encontrado no sistema.', 'warning')
    
    return render_template('auth/forgot_password.html', form=form)

@app.route('/redefinir-senha/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Página de redefinição de senha com token"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Buscar usuário com token válido
    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.verify_reset_token(token):
        flash('Token de recuperação inválido ou expirado.', 'danger')
        return redirect(url_for('login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Redefinir senha
        user.set_password(form.password.data)
        user.clear_reset_token()
        db.session.commit()
        
        flash('Senha redefinida com sucesso! Faça login com sua nova senha.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/reset_password.html', form=form, token=token)

# Rotas do Calculador
@app.route('/calculate')
@login_required
def calculate_redirect():
    """Redireciona para nova análise"""
    return redirect(url_for('new_calculation'))

@app.route('/nova-analise')
@login_required
def new_calculation():
    """Nova análise de importação"""
    product_form = ProductForm()
    cost_form = CostForm()
    
    # Obter cotação atual
    current_rate = currency_service.get_usd_brl_rate()
    
    return render_template('calculator/new_calculation.html', 
                         product_form=product_form,
                         cost_form=cost_form,
                         current_rate=current_rate)

@app.route('/calcular', methods=['POST'])
@login_required
def calculate():
    """Processar cálculo de importação"""
    product_form = ProductForm()
    cost_form = CostForm()
    
    if product_form.validate_on_submit() and cost_form.validate_on_submit():
        try:
            # Obter cotação atual
            exchange_rate = currency_service.get_usd_brl_rate()
            
            # Realizar cálculos
            calculation_result = tax_calculator.calculate_all_taxes(
                unit_value_usd=product_form.unit_value_usd.data,
                quantity=product_form.quantity.data,
                ncm_code=product_form.ncm_code.data,
                freight_usd=cost_form.freight_usd.data or 0,
                insurance_usd=cost_form.insurance_usd.data or 0,
                exchange_rate=exchange_rate
            )
            
            # Salvar no banco
            calculation = Calculation(
                user_id=current_user.id,
                product_name=product_form.product_name.data,
                ncm_code=product_form.ncm_code.data,
                description=product_form.description.data,
                unit_value_usd=product_form.unit_value_usd.data,
                quantity=product_form.quantity.data,
                origin_country=product_form.origin_country.data,
                transport_mode=product_form.transport_mode.data,
                exchange_rate=exchange_rate,
                total_cost_usd=calculation_result['customs_values']['cif_usd'],
                total_cost_brl=calculation_result['customs_values']['cif_brl'],
                total_taxes_brl=calculation_result['summary']['total_taxes'],
                final_cost_brl=calculation_result['summary']['total_cost']
            )
            
            db.session.add(calculation)
            db.session.flush()  # Para obter o ID
            
            # Salvar detalhes dos impostos
            for tax_type, tax_data in calculation_result['taxes'].items():
                tax_detail = TaxDetail(
                    calculation_id=calculation.id,
                    tax_type=tax_type,
                    rate=tax_data['rate'],
                    base_value=tax_data['base_value'],
                    amount=tax_data['amount']
                )
                db.session.add(tax_detail)
            
            # Salvar custos adicionais
            additional_costs = [
                ('FREIGHT', cost_form.freight_usd.data, cost_form.freight_usd.data * exchange_rate if cost_form.freight_usd.data else 0, 'Frete Internacional'),
                ('INSURANCE', cost_form.insurance_usd.data, cost_form.insurance_usd.data * exchange_rate if cost_form.insurance_usd.data else 0, 'Seguro'),
                ('CLEARANCE_FEES', None, cost_form.clearance_fees_brl.data or 0, 'Taxas de Desembaraço'),
                ('BROKER_FEES', None, cost_form.broker_fees_brl.data or 0, 'Honorários Despachante'),
                ('OTHER_COSTS', None, cost_form.other_costs_brl.data or 0, 'Outros Custos')
            ]
            
            for cost_type, amount_usd, amount_brl, description in additional_costs:
                if amount_brl and amount_brl > 0:
                    cost_detail = CostDetail(
                        calculation_id=calculation.id,
                        cost_type=cost_type,
                        amount_usd=amount_usd,
                        amount_brl=amount_brl,
                        description=description
                    )
                    db.session.add(cost_detail)
            
            db.session.commit()
            
            # Armazenar resultado na sessão
            session['last_calculation_id'] = calculation.id
            session['calculation_result'] = calculation_result
            
            flash('Cálculo realizado com sucesso!', 'success')
            return redirect(url_for('calculation_results', calc_id=calculation.id))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao realizar cálculo. Tente novamente.', 'danger')
            logging.error(f"Erro no cálculo: {str(e)}")
    
    # Se houve erros no formulário
    for field, errors in product_form.errors.items():
        for error in errors:
            flash(f'Erro no campo {field}: {error}', 'danger')
    
    for field, errors in cost_form.errors.items():
        for error in errors:
            flash(f'Erro no campo {field}: {error}', 'danger')
    
    current_rate = currency_service.get_usd_brl_rate()
    return render_template('calculator/new_calculation.html', 
                         product_form=product_form,
                         cost_form=cost_form,
                         current_rate=current_rate)

@app.route('/resultados/<calc_id>')
@login_required
def calculation_results(calc_id):
    """Visualizar resultados do cálculo"""
    calculation = Calculation.query.filter_by(id=calc_id, user_id=current_user.id).first_or_404()
    
    # Obter detalhes dos impostos e custos
    taxes = TaxDetail.query.filter_by(calculation_id=calc_id).all()
    costs = CostDetail.query.filter_by(calculation_id=calc_id).all()
    
    # Preparar dados para exibição
    tax_breakdown = {}
    for tax in taxes:
        tax_breakdown[tax.tax_type] = {
            'rate': tax.rate * 100,
            'base_value': tax.base_value,
            'amount': tax.amount
        }
    
    cost_breakdown = []
    for cost in costs:
        cost_breakdown.append({
            'type': cost.cost_type,
            'description': cost.description,
            'amount_usd': cost.amount_usd,
            'amount_brl': cost.amount_brl
        })
    
    profitability_form = ProfitabilityForm()
    scenario_form = ScenarioForm()
    
    return render_template('calculator/results.html', 
                         calculation=calculation,
                         taxes=tax_breakdown,
                         costs=cost_breakdown,
                         profitability_form=profitability_form,
                         scenario_form=scenario_form,
                         currency_service=currency_service)

@app.route('/calcular-rentabilidade/<calc_id>', methods=['POST'])
@login_required
def calculate_profitability(calc_id):
    """Calcular rentabilidade"""
    calculation = Calculation.query.filter_by(id=calc_id, user_id=current_user.id).first_or_404()
    form = ProfitabilityForm()
    
    if form.validate_on_submit():
        try:
            # Calcular rentabilidade
            profitability_result = tax_calculator.calculate_profitability(
                total_cost_brl=calculation.final_cost_brl,
                selling_price_brl=form.selling_price_brl.data,
                additional_costs={
                    'storage': form.storage_cost_brl.data or 0,
                    'marketing': form.marketing_cost_brl.data or 0,
                    'platform_fees_rate': form.platform_fees_rate.data or 0
                }
            )
            
            # Atualizar cálculo
            calculation.suggested_price = form.selling_price_brl.data
            calculation.expected_revenue = profitability_result['net_profit']
            calculation.profit_margin = profitability_result['net_margin']
            
            db.session.commit()
            
            # Armazenar resultado na sessão
            session['profitability_result'] = profitability_result
            
            return jsonify({
                'success': True,
                'data': profitability_result
            })
            
        except Exception as e:
            logging.error(f"Erro no cálculo de rentabilidade: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Erro ao calcular rentabilidade'
            }), 500
    
    return jsonify({
        'success': False,
        'error': 'Dados inválidos'
    }), 400

@app.route('/historico')
@login_required
def calculation_history():
    """Histórico de cálculos"""
    page = request.args.get('page', 1, type=int)
    calculations = Calculation.query.filter_by(user_id=current_user.id)\
                                   .order_by(Calculation.created_at.desc())\
                                   .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('calculator/history.html', calculations=calculations)

@app.route('/cenarios')
@login_required
def saved_scenarios():
    """Cenários salvos"""
    scenarios = ProductScenario.query.filter_by(user_id=current_user.id)\
                                   .order_by(ProductScenario.created_at.desc()).all()
    
    return render_template('calculator/scenarios.html', scenarios=scenarios)

@app.route('/salvar-cenario/<calc_id>', methods=['POST'])
@login_required
def save_scenario(calc_id):
    """Salvar cenário"""
    calculation = Calculation.query.filter_by(id=calc_id, user_id=current_user.id).first_or_404()
    form = ScenarioForm()
    
    if form.validate_on_submit():
        try:
            scenario = ProductScenario(
                user_id=current_user.id,
                name=form.name.data,
                ncm_code=calculation.ncm_code,
                description=calculation.description,
                unit_value_usd=calculation.unit_value_usd,
                origin_country=calculation.origin_country,
                transport_mode=calculation.transport_mode,
                exchange_rate=calculation.exchange_rate,
                default_quantity=calculation.quantity
            )
            
            db.session.add(scenario)
            db.session.commit()
            
            flash('Cenário salvo com sucesso!', 'success')
            return jsonify({'success': True})
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Erro ao salvar cenário: {str(e)}")
            return jsonify({'success': False, 'error': 'Erro ao salvar cenário'}), 500
    
    return jsonify({'success': False, 'error': 'Nome inválido'}), 400

# APIs de apoio
@app.route('/api/ncm/buscar')
def api_search_ncm():
    """API para buscar códigos NCM"""
    try:
        query = request.args.get('q', '').strip()
        if len(query) < 2:
            return jsonify([])
        
        results = ncm_service.search_ncm(query)
        return jsonify(results)
    except Exception as e:
        logging.error(f"Erro na busca NCM: {str(e)}")
        return jsonify({"error": "Erro interno na busca de códigos NCM"}), 500

@app.route('/api/ncm/<ncm_code>')
@login_required
def api_get_ncm(ncm_code):
    """API para obter informações de um NCM"""
    ncm_info = ncm_service.get_ncm_info(ncm_code)
    if ncm_info:
        return jsonify(ncm_info)
    return jsonify({'error': 'NCM não encontrado'}), 404

@app.route('/api/cotacao')
@login_required
def api_get_exchange_rate():
    """API para obter cotação atual"""
    rate = currency_service.get_usd_brl_rate()
    return jsonify({
        'rate': rate,
        'formatted': currency_service.format_currency_brl(rate)
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
