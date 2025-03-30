import os

# class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://incomexpense_user:YAOGv0GNJZ3gu2eKByr6kxNHfmPfCB4d@dpg-cvdgu0pc1ekc73e1i1gg-a/incomexpense")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
def get_env_var(var_name):
    """Helper function to get env variables, preferring _ prefixed ones if available."""
    return os.getenv(f"_{var_name}") or os.getenv(var_name)

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{get_env_var('DB_USER')}:{get_env_var('DB_PASSWORD')}"
        f"@{get_env_var('DB_HOST')}:{get_env_var('DB_PORT')}/{get_env_var('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
