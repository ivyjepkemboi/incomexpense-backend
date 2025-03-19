import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://incomexpense_user:YAOGv0GNJZ3gu2eKByr6kxNHfmPfCB4d@dpg-cvdgu0pc1ekc73e1i1gg-a/incomexpense")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
