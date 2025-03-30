from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS  # Import CORS
from config import Config
from db import db
from routes.auth_routes import auth_routes
from routes.expense_routes import expense_routes

app = Flask(__name__)

app.config.from_object(Config)

# db.init_app(app)
jwt = JWTManager(app)
# migrate = Migrate(app, db)

CORS(app)  # Enable CORS for all routes

app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(expense_routes, url_prefix='/api')


if __name__ == "__main__":
    app.run(debug=True,port=8080,host="0.0.0.0")
