from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from energyWebapp.apps.baseApp.models.user import User
from energyWebapp.apps.baseApp.routes import base
from energyWebapp.apps.historyApp.routes import history
from energyWebapp.apps.batteryApp.routes import battery
from energyWebapp.general.db.extensions import db

def create_app():
    appl = Flask(__name__, static_folder='energyWebapp/apps/baseApp/static', static_url_path='/base')
    appl.config['SECRET_KEY'] = 'test'
    appl.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://master2025:anwendungssysteme@db.kaidro.de:5432/postgres'
    appl.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



    db.init_app(appl)
    
    login_manager = LoginManager()
    login_manager.init_app(appl)
    login_manager.login_view = 'base.login_view'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    appl.register_blueprint(base, url_prefix='/')
    appl.register_blueprint(history, url_prefix='/history')
    appl.register_blueprint(battery, url_prefix='/battery')
    return appl

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

