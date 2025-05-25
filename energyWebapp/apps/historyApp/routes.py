from flask import Blueprint, render_template, redirect, url_for
from energyWebapp.apps.baseApp.models.electricityhistory import ElectricityPriceHistory


history = Blueprint('history', __name__, template_folder='templates', static_url_path='static' ,static_folder='static')

# -------------------------------------------------------------------
#                          Web-UI Routen
# -------------------------------------------------------------------
# Home Ansicht
@history.route('/', methods=['GET'])
def history_view():
    prices = ElectricityPriceHistory.get_prices()
    return render_template('history.html', prices=prices["prices_euro"], timestamps=prices["timestamps"])

# -------------------------------------------------------------------
#                        REST-API Routen
# -------------------------------------------------------------------

# Müssen noch implementiert werden, speziell interaktion mit der DB und dem ChartJS