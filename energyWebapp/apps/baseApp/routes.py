from flask import Blueprint, render_template, redirect, url_for

base = Blueprint('base', __name__, template_folder='templates')

# -------------------------------------------------------------------
#                          Web-UI Routen
# -------------------------------------------------------------------
# Home Redirect
@base.route('/', methods=['GET'])
def index():
    return redirect(url_for('base.home_view'))

# Home Ansicht
@base.route('/home', methods=['GET'])
def home_view():
    return render_template('home.html')

# Login Ansicht
@base.route('/login', methods=['GET'])
def login_view1():
    return render_template('login.html')

# Register Ansicht
@base.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')

# Account Ansicht
@base.route('/register', methods=['GET'])
def account_view():
    return render_template('account.html')

# -------------------------------------------------------------------
#                        REST-API Routen
# -------------------------------------------------------------------

# Werdeb noch implementiert, speziell Login, Register usw. außer das wird über js gemacht