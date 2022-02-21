from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

#init my login LoginManager
login = LoginManager()

#inits for the database stuff
db = SQLAlchemy()
migrate = Migrate(db,compare_type=True)
moment = Moment()

def create_app(config_class=Config):
    #init the app
    app = Flask(__name__)
    #linking our config to the app
    app.config.from_object(Config)

    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    #this is where you will be sent if you are not logged in
    login.login_view='login'

    moment.init_app(app)

    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.shop import bp as shop_bp
    app.register_blueprint(shop_bp)

    return app
