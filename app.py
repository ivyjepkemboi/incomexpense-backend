from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql
import os
from flask.cli import with_appcontext
import click

# Initialize Flask app
app = Flask(__name__)

# Database Configuration (Replace these with your actual values)
PASSWORD = "achawee.123!*"
DBNAME = "expenses"
PROJECT_ID = "landser"
INSTANCE_NAME = "expense"

# Set up the connection URL for Cloud SQL (using PyMySQL as the driver)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://exp_admin:{PASSWORD}@/"
    f"{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:us-central1:{INSTANCE_NAME}"
)

# Other Flask configurations
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database object and Migrate object
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models (ensure this is done after db is initialized)
from models import *

@app.route('/')
def test_connection():
    try:
        # Attempt to execute a simple query to check the connection
        result = db.session.execute("SELECT 1")
        row = result.fetchone()  # Fetch the first row
        return jsonify({"message": "Connection successful", "result": row[0]}), 200
    except pymysql.MySQLError as e:
        return jsonify({"error": "Database connection failed", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Add a custom command to run migrations automatically on startup
@app.cli.command('migrate_on_start')
@with_appcontext
def migrate_on_start():
    """Automatically run migrations on app load"""
    try:
        print("Running migrations...")
        # Automatically apply migrations
        click.echo("Running migrations...")
        from flask_migrate import upgrade
        upgrade()
        print("Migrations applied successfully!")
    except Exception as e:
        print(f"Error applying migrations: {e}")

if __name__ == '__main__':
    app.run(debug=True)
