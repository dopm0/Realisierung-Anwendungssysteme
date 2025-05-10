from flask import Blueprint, render_template, redirect, url_for

battery = Blueprint('battery', __name__, template_folder='templates', static_url_path='static' ,static_folder='static')

# -------------------------------------------------------------------
#                          Web-UI Routen
# -------------------------------------------------------------------
# Home Ansicht
@battery.route('/battery', methods=['GET'])
def battery_view():
    return render_template('battery.html')
# -------------------------------------------------------------------
#                        REST-API Routen
# -------------------------------------------------------------------

# Müssen noch implementiert werden, speziell interaktion mit der DB und Backend für Berechnungen zur optimalen Speichergröße und Stromersparnissen