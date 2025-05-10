from flask import Flask
from energyWebapp.apps.baseApp.routes import base
from energyWebapp.apps.baseApp.routes import history
from energyWebapp.apps.baseApp.routes import battery

def create_app():
    appl = Flask(__name__, static_folder='Apps/baseApp/static', static_url_path='/base')
    appl.register_blueprint(base, url_prefix='/')
    appl.register_blueprint(history, url_prefix='/history')
    appl.register_blueprint(battery, url_prefix='/battery')
    return appl

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)

