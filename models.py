from db import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    
    # Fields for Expenses
    category = db.Column(db.String(50), nullable=True)  # Only for expenses
    subcategory = db.Column(db.String(50), nullable=True)  # Only for expenses
    title = db.Column(db.String(100), nullable=True)  # Only for expenses
    
    # Fields for Income
    source = db.Column(db.String(100), nullable=True)  # Only for income
    
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))