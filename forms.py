from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo, Optional
from wtforms.widgets import NumberInput

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()], 
                       render_kw={'placeholder': 'seu@email.com', 'class': 'form-control'})
    password = PasswordField('Senha', validators=[DataRequired()], 
                           render_kw={'placeholder': 'Digite sua senha', 'class': 'form-control'})
    submit = SubmitField('Entrar', render_kw={'class': 'btn btn-primary w-100'})

class RegisterForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=100)], 
                      render_kw={'placeholder': 'Seu nome completo', 'class': 'form-control'})
    email = StringField('E-mail', validators=[DataRequired(), Email()], 
                       render_kw={'placeholder': 'seu@email.com', 'class': 'form-control'})
    company = StringField('Empresa (Opcional)', validators=[Optional(), Length(max=200)], 
                         render_kw={'placeholder': 'Nome da sua empresa', 'class': 'form-control'})
    user_type = SelectField('Tipo de Usuário', 
                           choices=[('IMPORTER', 'Importador'), ('TAX_CONSULTANT', 'Consultor Tributário')],
                           validators=[DataRequired()], render_kw={'class': 'form-select'})
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)], 
                           render_kw={'placeholder': 'Mínimo 6 caracteres', 'class': 'form-control'})
    password2 = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais')], 
                            render_kw={'placeholder': 'Digite a senha novamente', 'class': 'form-control'})
    submit = SubmitField('Criar Conta', render_kw={'class': 'btn btn-primary w-100'})

class ProductForm(FlaskForm):
    product_name = StringField('Nome do Produto', validators=[DataRequired(), Length(max=200)], 
                              render_kw={'placeholder': 'Ex: Smartphone Samsung Galaxy', 'class': 'form-control'})
    ncm_code = StringField('Código NCM', validators=[DataRequired(), Length(min=8, max=10)], 
                          render_kw={'placeholder': 'Ex: 85171200', 'class': 'form-control', 'list': 'ncm-suggestions'})
    description = TextAreaField('Descrição (Opcional)', validators=[Optional()], 
                               render_kw={'placeholder': 'Descrição detalhada do produto', 'class': 'form-control', 'rows': 3})
    unit_value_usd = FloatField('Valor Unitário (USD)', validators=[DataRequired(), NumberRange(min=0.01)], 
                               widget=NumberInput(step=0.01), render_kw={'placeholder': '0.00', 'class': 'form-control'})
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)], 
                           render_kw={'placeholder': '1', 'class': 'form-control', 'value': '1'})
    origin_country = StringField('País de Origem', validators=[DataRequired(), Length(max=100)], 
                                render_kw={'placeholder': 'Ex: China', 'class': 'form-control'})
    transport_mode = SelectField('Modalidade de Transporte', 
                                choices=[('MARITIME', 'Marítimo'), ('AIR', 'Aéreo'), ('ROAD', 'Rodoviário')],
                                validators=[DataRequired()], render_kw={'class': 'form-select'})

class CostForm(FlaskForm):
    freight_usd = FloatField('Frete Internacional (USD)', validators=[Optional(), NumberRange(min=0)], 
                            widget=NumberInput(step=0.01), render_kw={'placeholder': '0.00', 'class': 'form-control', 'value': '0'})
    insurance_usd = FloatField('Seguro (USD)', validators=[Optional(), NumberRange(min=0)], 
                              widget=NumberInput(step=0.01), render_kw={'placeholder': '0.00', 'class': 'form-control', 'value': '0'})
    clearance_fees_brl = FloatField('Taxas de Desembaraço (BRL)', validators=[Optional(), NumberRange(min=0)], 
                                   widget=NumberInput(step=0.01), render_kw={'placeholder': '0.00', 'class': 'form-control', 'value': '0'})
    broker_fees_brl = FloatField('Honorários Despachante (BRL)', validators=[Optional(), NumberRange(min=0)], 
                                widget=NumberInput(step=0.01), render_kw={'placeholder': '0.00', 'class': 'form-control', 'value': '0'})
    storage_cost_brl = FloatField('Custo de Armazenagem (BRL)', validators=[Optional(), NumberRange(min=0)], 
                                 widget=NumberInput(step=0.01), render_kw={'placeholder': '0.00', 'class': 'form-control', 'value': '0'})
    marketing_cost_brl = FloatField('Custo de Marketing (BRL)', validators=[Optional(), NumberRange(min=0)], 
                                   widget=NumberInput(step=0.01), render_kw={'placeholder': '0.00', 'class': 'form-control', 'value': '0'})
    other_costs_brl = FloatField('Outros Custos (BRL)', validators=[Optional(), NumberRange(min=0)], 
                                widget=NumberInput(step=0.01), render_kw={'placeholder': '0.00', 'class': 'form-control', 'value': '0'})

class ProfitabilityForm(FlaskForm):
    selling_price_brl = FloatField('Preço de Venda Desejado (BRL)', validators=[DataRequired(), NumberRange(min=0.01)], 
                                  widget=NumberInput(step=0.01), render_kw={'placeholder': '0.00', 'class': 'form-control'})
    submit = SubmitField('Calcular Rentabilidade', render_kw={'class': 'btn btn-success'})

class ScenarioForm(FlaskForm):
    name = StringField('Nome do Cenário', validators=[DataRequired(), Length(max=200)], 
                      render_kw={'placeholder': 'Ex: iPhone 15 Pro China', 'class': 'form-control'})
    submit = SubmitField('Salvar Cenário', render_kw={'class': 'btn btn-primary'})

class ForgotPasswordForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()], 
                       render_kw={'placeholder': 'seu@email.com', 'class': 'form-control'})
    submit = SubmitField('Enviar Link de Recuperação', render_kw={'class': 'btn btn-primary w-100'})

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=6)], 
                           render_kw={'placeholder': 'Mínimo 6 caracteres', 'class': 'form-control'})
    password2 = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais')], 
                            render_kw={'placeholder': 'Digite a senha novamente', 'class': 'form-control'})
    submit = SubmitField('Redefinir Senha', render_kw={'class': 'btn btn-success w-100'})
