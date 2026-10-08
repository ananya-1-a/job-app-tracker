import os
from dotenv import load_dotenv
from flask import Flask,jsonify
from config import config
from extensions import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models.company import Company 
from flasgger import Swagger
import sys
load_dotenv()
print(f"PYTHONPATH: {sys.path}")
print(f"DATABASE_URL_LOADED: {os.getenv('DATABASE_URL') is not None}")

def create_app(config_name="default"):
    # 1. Initialize the app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,  
    "pool_recycle": 300,    
    }
    
    
    db.init_app(app)
    migrate=Migrate(app,db)

    jwt=JWTManager(app)
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Job Application & AI Coach API",
            "description": "A production-grade backend for tracking applications and generating AI interview prep.",
            "version": "1.0.0"
        },
        "schemes": [
            "https",
            "http"
        ],
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter the word 'Bearer' followed by a space and then your JWT token. Example: Bearer eyJhb..."
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ]
    }
    Swagger(app, template=swagger_template)
    from routes.company_routes import company_bp
    app.register_blueprint(company_bp)
    
    from routes.application_routes import application_bp
    app.register_blueprint(application_bp)

    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error":"Route not found"}),404
    
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error":"Internal server error"}),500
    
    @ jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_data):
        return jsonify({"error":"Token has expired"}),401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"error":"Missing or invalid token"}),401
    
    @jwt.unauthorized_loader
    def unauthorized_token_callback(reason):
        return jsonify({"error":"Unauthorized token"}),401
    
    # 3. Build the Database
    with app.app_context():
        from models.user import User
        from models.company import Company
        from models.job_application import JobApplication
        db.create_all()
    return app
app = create_app()
if __name__ == "__main__":
    
    app.run(debug=True)