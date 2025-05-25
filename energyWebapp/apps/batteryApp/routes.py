from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from energyWebapp.apps.baseApp.models.electricityhistory import ElectricityPriceHistory
from energyWebapp.apps.baseApp.models.electricitycost import ElectricityCost

battery = Blueprint('battery', __name__, template_folder='templates', static_url_path='static' ,static_folder='static')

# -------------------------------------------------------------------
#                          Web-UI Routen
# -------------------------------------------------------------------
# Home Ansicht
@battery.route('/', methods=['GET'])
@login_required
def battery_view():
    return render_template('battery.html', data=current_user.electricity_cost)
# -------------------------------------------------------------------
#                        REST-API Routen
# -------------------------------------------------------------------

# Müssen noch implementiert werden, speziell interaktion mit der DB und Backend für Berechnungen zur optimalen Speichergröße und Stromersparnissen

@battery.route('/calc', methods=['POST'])
@login_required
def calc_data():
    consumption    = request.form.get('consumption', '').replace(',', '.')
    price          = request.form.get('price', '').replace(',', '.')
    print(price, consumption)
    cost_entry  = current_user.electricity_cost

    if (cost_entry.electricity_consumption_user == consumption and
            cost_entry.electricity_price_user == price):
        return render_template('battery_data.html', data=cost_entry)
    else:
        optimized = ElectricityPriceHistory.calculate_optimized_cost(
            electricity_price_user=float(price),
            electricity_consumption_user=float(consumption),
            cost_entry=cost_entry
        )
        print(optimized)
    
    return redirect(url_for('battery.battery_view'))