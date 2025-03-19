import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin@localhost:5432/expense_tracker"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key"

