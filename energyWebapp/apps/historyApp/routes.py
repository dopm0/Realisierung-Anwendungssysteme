from flask import Blueprint, render_template, redirect, url_for

history = Blueprint('history', __name__, template_folder='templates', static_url_path='static' ,static_folder='static')

# -------------------------------------------------------------------
#                          Web-UI Routen
# -------------------------------------------------------------------
# Home Ansicht
@history.route('/history', methods=['GET'])
def history_view():
    return render_template('history.html')
# -------------------------------------------------------------------
#                        REST-API Routen
# -------------------------------------------------------------------

# Müssen noch implementiert werden, speziell interaktion mit der DB und dem ChartJS