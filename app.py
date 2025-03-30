from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
import os

from sqlalchemy import text

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

# Initialize the database object
db = SQLAlchemy(app)

@app.route('/')

def test_connection():
    try:
        # Attempt to execute a simple query to check the connection
        result = db.session.execute("SELECT 1")
        row = result.fetchone()  # Fetch the first row
        return jsonify({"message": "Connection successful", "result": row[0]}), 200  # Access the first column
    except pymysql.MySQLError as e:
        # Handle errors related to MySQL connection
        return jsonify({"error": "Database connection failed", "details": str(e)}), 500
    except Exception as e:
        # Handle any other unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    try:
        # Check connection at app startup
        db.session.execute(text("SELECT * 1"))
       
        print("Database connection successful.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")
    app.run(debug=True)
