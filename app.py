from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS  # Import CORS
from config import Config
from db import db
from routes.auth_routes import auth_routes
from routes.expense_routes import expense_routes
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# Google Cloud SQL Configuration (Update accordingly)
PASSWORD = "achawee.123!*"
PUBLIC_IP_ADDRESS = "4.57.129.2"  # If using public IP (optional, or replace with Cloud SQL socket)
DBNAME = "expenses"
PROJECT_ID = "landser"
INSTANCE_NAME = "expense"

# Configuration
app.config["SECRET_KEY"] = "yoursecretkey"

# Correct SQLAlchemy connection string
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+mysqldb://exp_admin:{PASSWORD}@/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
)

# Optional: Disable track modifications if not needed
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# app.config.from_object(Config)

# db.init_app(app)
jwt = JWTManager(app)
# migrate = Migrate(app, db)

CORS(app)  # Enable CORS for all routes

app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(expense_routes, url_prefix='/api')

@app.route("/")
def home():
    return "Hello, Cloud Run!"


if __name__ == "__main__":
    app.run(debug=True,port=8080,host="0.0.0.0")
