from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

battery = Blueprint('battery', __name__, template_folder='templates', static_url_path='static' ,static_folder='static')

# -------------------------------------------------------------------
#                          Web-UI Routen
# -------------------------------------------------------------------
# Home Ansicht
@battery.route('/', methods=['GET'])
@login_required
def battery_view():
    verbrauch= 3500
    strompreis = 0.35
    return render_template('battery.html', verbrauch=verbrauch, strompreis=strompreis)
# -------------------------------------------------------------------
#                        REST-API Routen
# -------------------------------------------------------------------

# Müssen noch implementiert werden, speziell interaktion mit der DB und Backend für Berechnungen zur optimalen Speichergröße und Stromersparnissen