from main import create_app
from energyWebapp.general.db.extensions import db  # falls du extensions.py verwendest

app = create_app()

with app.app_context():
    db.create_all()
    print("User-Tabelle erfolgreich im Schema 'mw212_projekt' erstellt.")
