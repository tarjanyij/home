from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bs4 import Bootstrap

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def page_not_found():
        return render_template('error/404.html'),404

def internal_server_error(e):
        return render_template('error/500.html', error_text=e),500

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'Titokos_kulcs_12345'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tempwriter:Titok12345@192.168.8.250/home'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    Migrate(app, db)
    Bootstrap(app)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # blueprint registration api
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # blueprint registration api
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app