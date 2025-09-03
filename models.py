from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(datetime.now().timestamp()).replace('.', ''))
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    company = db.Column(db.String(200), nullable=True)
    user_type = db.Column(db.Enum('IMPORTER', 'TAX_CONSULTANT', 'ADMIN', name='user_type'), default='IMPORTER')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    calculations = db.relationship('Calculation', backref='user', lazy=True, cascade='all, delete-orphan')
    product_scenarios = db.relationship('ProductScenario', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Calculation(db.Model):
    __tablename__ = 'calculations'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(datetime.now().timestamp()).replace('.', ''))
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    scenario_id = db.Column(db.String, db.ForeignKey('product_scenarios.id'), nullable=True)
    product_name = db.Column(db.String(200), nullable=False)
    ncm_code = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=True)
    unit_value_usd = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    origin_country = db.Column(db.String(100), nullable=False)
    transport_mode = db.Column(db.Enum('MARITIME', 'AIR', 'ROAD', name='transport_mode'), nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)
    total_cost_usd = db.Column(db.Float, nullable=False)
    total_cost_brl = db.Column(db.Float, nullable=False)
    total_taxes_brl = db.Column(db.Float, nullable=False)
    final_cost_brl = db.Column(db.Float, nullable=False)
    suggested_price = db.Column(db.Float, nullable=True)
    expected_revenue = db.Column(db.Float, nullable=True)
    profit_margin = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    taxes = db.relationship('TaxDetail', backref='calculation', lazy=True, cascade='all, delete-orphan')
    costs = db.relationship('CostDetail', backref='calculation', lazy=True, cascade='all, delete-orphan')

class TaxDetail(db.Model):
    __tablename__ = 'tax_details'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(datetime.now().timestamp()).replace('.', ''))
    calculation_id = db.Column(db.String, db.ForeignKey('calculations.id'), nullable=False)
    tax_type = db.Column(db.Enum('II', 'IPI', 'PIS', 'COFINS', 'ICMS', 'OTHERS', name='tax_type'), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    base_value = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CostDetail(db.Model):
    __tablename__ = 'cost_details'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(datetime.now().timestamp()).replace('.', ''))
    calculation_id = db.Column(db.String, db.ForeignKey('calculations.id'), nullable=False)
    cost_type = db.Column(db.Enum('FREIGHT', 'INSURANCE', 'CLEARANCE_FEES', 'BROKER_FEES', 'STORAGE', 'DOMESTIC_FREIGHT', 'MARKETING', 'PLATFORM_FEES', 'OTHER_COSTS', name='cost_type'), nullable=False)
    amount_usd = db.Column(db.Float, nullable=True)
    amount_brl = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ProductScenario(db.Model):
    __tablename__ = 'product_scenarios'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(datetime.now().timestamp()).replace('.', ''))
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    ncm_code = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=True)
    unit_value_usd = db.Column(db.Float, nullable=False)
    origin_country = db.Column(db.String(100), nullable=False)
    transport_mode = db.Column(db.Enum('MARITIME', 'AIR', 'ROAD', name='transport_mode'), nullable=False)
    exchange_rate = db.Column(db.Float, nullable=True)
    default_quantity = db.Column(db.Integer, default=1)
    freight_cost = db.Column(db.Float, nullable=True)
    insurance_cost = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NcmCache(db.Model):
    __tablename__ = 'ncm_cache'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(datetime.now().timestamp()).replace('.', ''))
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    ii_rate = db.Column(db.Float, nullable=True)
    ipi_rate = db.Column(db.Float, nullable=True)
    pis_rate = db.Column(db.Float, nullable=True)
    cofins_rate = db.Column(db.Float, nullable=True)
    icms_rate = db.Column(db.Float, nullable=True)
    ex = db.Column(db.Integer, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

class ExchangeRateHistory(db.Model):
    __tablename__ = 'exchange_rate_history'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(datetime.now().timestamp()).replace('.', ''))
    currency = db.Column(db.String(3), default='USD')
    rate = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemConfig(db.Model):
    __tablename__ = 'system_config'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(datetime.now().timestamp()).replace('.', ''))
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
