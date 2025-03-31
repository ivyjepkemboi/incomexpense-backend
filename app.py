import click
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS  # Import CORS
from config import Config
from db import db
from routes.auth_routes import auth_routes
from routes.expense_routes import expense_routes
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os
from flask_bcrypt import Bcrypt
from models import User, Transaction  # Import the models

app = Flask(__name__)

# Database Configuration (Replace these with your actual values)
PASSWORD = "achawee.123!*"
DBNAME = "expenses"
PROJECT_ID = "landser"
INSTANCE_NAME = "expense"
USER = "exp_admin"

# Set up the connection URL for Cloud SQL (using PyMySQL as the driver)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{USER}:{PASSWORD}@/"
    f"{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:us-central1:{INSTANCE_NAME}"
)

# Other Flask configurations
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False




# Initialize the database instance with Flask app
db.init_app(app)

# Initialize Flask-Migrate with app and db
migrate = Migrate(app, db)


jwt = JWTManager(app)

bcrypt = Bcrypt()

CORS(app)  # Enable CORS for all routes

app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(expense_routes, url_prefix='/api')


@app.route('/')

def test_connection():
    try:
        # Attempt to execute a simple query to check the connection
        result = db.session.execute(text("SELECT 1"))
        row = result.fetchone()  # Fetch the first row
        return jsonify({"message": "Connection successful", "result": row[0]}), 200  # Access the first column
    except pymysql.MySQLError as e:
        # Handle errors related to MySQL connection
        return jsonify({"error": "Database connection failed", "details": str(e)}), 500
    except Exception as e:
        # Handle any other unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
        
# Define the /create_tables route to create all tables
@app.route('/c')
def create_tables():
    try:
        # Create all tables based on the models defined
        db.create_all()

        # Optionally, you can add sample data here if you want to populate the tables with data

        return jsonify({"message": "Tables created successfully!"}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while creating tables.", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True,port=8080,host="0.0.0.0")
