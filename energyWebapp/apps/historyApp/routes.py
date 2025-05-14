from flask import Blueprint, render_template, redirect, url_for

history = Blueprint('history', __name__, template_folder='templates', static_url_path='static' ,static_folder='static')

# -------------------------------------------------------------------
#                          Web-UI Routen
# -------------------------------------------------------------------
# Home Ansicht
@history.route('/history', methods=['GET'])
def history_view():
    verbrauch= 3500
    strompreis = 0.35
    return render_template('history.html', verbrauch=verbrauch, strompreis=strompreis)

@history.route('/historyMap', methods=['GET'])
def historyMap_view():
    return render_template('historyMap.html')
# -------------------------------------------------------------------
#                        REST-API Routen
# -------------------------------------------------------------------

# Müssen noch implementiert werden, speziell interaktion mit der DB und dem ChartJS