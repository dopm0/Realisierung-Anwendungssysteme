from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from energyWebapp.apps.batteryApp.models.electricitycost import ElectricityCost
from energyWebapp.apps.baseApp.models.user import User
from energyWebapp.general.db.extensions import db

base = Blueprint('base', __name__, template_folder='templates')

# -------------------------------------------------------------------
#                          Web-UI Routen
# -------------------------------------------------------------------
# Home Redirect
@base.route('/', methods=['GET'])
def index():
    return redirect('/home')

# Home Ansicht
@base.route('/home', methods=['GET'])
def home_view():
    return render_template('home.html')

# Login Ansicht
@base.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

# Registrieren Ansicht
@base.route('/register', methods=['GET'])
def register_view():
    if current_user.is_authenticated:
        return redirect(url_for('base.konto_view'))
    return render_template('register.html')

@base.route('/konto', methods=['GET'])
@login_required
def konto_view():
    return render_template('konto.html', user=current_user, data=current_user.electricity_cost)

# -------------------------------------------------------------------
#                        REST-API Routen
# -------------------------------------------------------------------
# Route für Anmeldung
@base.route('/login', methods=['POST'])
def login_func():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(Username=username).first()

    # Authentifizierung prüfen
    if user and user.Password == password:
        login_user(user)
        return redirect(url_for('base.konto_view'))  # Zielseite nach Login
    else:
        flash('Ungültige Anmeldedaten')
        return redirect(url_for('base.login_view'))  # Zurück zur Login-Seite
    
# Route für Abmeldung
@base.route('/logout')
@login_required
def logout_func():
    logout_user()
    return redirect(url_for('base.home_view'))  # Zurück zur Startseite

@base.route('/register', methods=['POST'])
def register_func():
    username = request.form.get('username')
    password = request.form.get('password')

    # Benutzername prüfen
    existing_user = User.query.filter_by(Username=username).first()
    if existing_user:
        flash('Benutzername bereits vergeben')
        return redirect(url_for('base.register_view'))

    # Benutzer erstellen
    new_user = User(Username=username, Password=password)
    db.session.add(new_user)
    db.session.commit()

    # Zum Nutzer gehörige ElectricityCost erstellen
    data = ElectricityCost(user_id=new_user.ID_User)
    db.session.add(data)
    db.session.commit()

    flash('Registrierung erfolgreich – bitte einloggen')
    return redirect(url_for('base.login_view'))

#Route zum Speichern von Benutzerdaten
@base.route('/userdata', methods=['POST'])
def save_userdata():
    consumption    = request.form.get('consumption', '').replace(',', '.')
    price          = request.form.get('price', '').replace(',', '.')

    cost_entry  = current_user.electricity_cost
    
    cost_entry.electricity_consumption_user = float(consumption)
    cost_entry.electricity_price_user       = float(price)

    db.session.commit()

    return redirect(url_for('base.konto_view'))