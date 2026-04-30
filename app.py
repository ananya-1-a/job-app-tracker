import os
from dotenv import load_dotenv
from flask import Flask
from config import config
from extensions import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models.company import Company 
load_dotenv()
def create_app():
    # 1. Initialize the app
    app = Flask(__name__)
    app.config.from_object(config)

    app.config['SQLALCHEMY_DATABSE_URI']='sqlite:///job_tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    app.config['JWT_SECRET_KEY']= os.getenv('JWT_SECRET_KEY')
    
    
    db.init_app(app)
    migrate=Migrate(app,db)

    jwt=JWTManager(app)
    from routes.company_routes import company_bp
    app.register_blueprint(company_bp)
    
    from routes.application_routes import application_bp
    app.register_blueprint(application_bp)

    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    # 3. Build the Database
    with app.app_context():
        from models.user import User
        from models.company import Company
        from models.job_application import JobApplication
        db.create_all()
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)