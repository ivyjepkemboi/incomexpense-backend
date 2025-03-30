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



# Define a simple User model for the table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Route to create the table and populate it with data
@app.route('/create_table')
def create_table():
    try:
        # Create the table in the database
        db.create_all()

        # Populate the table with some data if it's empty
        if User.query.count() == 0:
            user1 = User(username='alice', email='alice@example.com')
            user2 = User(username='bob', email='bob@example.com')
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

        return jsonify({"message": "Table created and data inserted"}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

# Route to select and show all users
@app.route('/show_users')
def show_users():
    try:
        # Query all users from the User table
        users = User.query.all()

        # Format the result as a list of dictionaries
        users_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]

        return jsonify({"users": users_list}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching data", "details": str(e)}), 500

# Route to test connection to the database



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

if __name__ == '__main__':
    try:
        # Check connection at app startup
        db.session.execute(text("SELECT * 1"))
       
        print("Database connection successful.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")
    app.run(debug=True)
