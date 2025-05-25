import asyncio
import asyncpg
from datetime import datetime, timedelta

# === Verbindung zur Datenbank ===
DB_USER = "master2025"
DB_PASS = "anwendungssysteme"
DB_HOST = "db.kaidro.de"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_SCHEMA = "mw212_projekt"
TABLE_HISTORY = "electricity_price_history"

async def get_avg_daily_lowest_price_last_year():
    """Ermittelt den durchschnittlichen Tages-Tiefstpreis in €/MWh."""
    try:
        today = datetime.today()
        one_year_ago = today - timedelta(days=365)

        conn = await asyncpg.connect(
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT
        )
        await conn.execute(f"SET search_path TO {DB_SCHEMA};")

        query = f"""
            SELECT AVG(daily_min) AS avg_daily_min_price
            FROM (
                SELECT DATE("timestamp") AS tag, MIN("price_euro") AS daily_min
                FROM {TABLE_HISTORY}
                WHERE "timestamp" BETWEEN $1 AND $2
                GROUP BY DATE("timestamp")
            ) t;
        """
        result = await conn.fetchval(query, one_year_ago, today)
        await conn.close()

        return float(result) if result is not None else None

    except Exception as e:
        print("Fehler beim Abrufen des durchschnittlichen Tages-Tiefstpreises:", e)
        return None

async def calculate_optimized_cost(user_id, electricity_price_user, electricity_consumption_user):
    """
    Berechnet optimierte Stromkosten basierend auf dem durchschnittlichen Tages-Tiefstpreis.
    Preis in €/kWh, Verbrauch in kWh/Jahr
    """
    try:
        electricity_cost_user = electricity_price_user * electricity_consumption_user
        NetworkFees = 0.12

        lowest_avg_price_mwh = await get_avg_daily_lowest_price_last_year()
        if lowest_avg_price_mwh is None:
            raise ValueError("Preis konnte nicht ermittelt werden.")

        # €/MWh in €/kWh umrechnen
        lowest_price_kwh = lowest_avg_price_mwh / 1000

        electricity_cost_optimized = (lowest_price_kwh + NetworkFees) * electricity_consumption_user 
        savings = electricity_cost_user - electricity_cost_optimized

        battery = electricity_consumption_user / 365
        return {
            "user_id": user_id,
            "electricity_price_user": electricity_price_user,
            "electricity_consumption_user": electricity_consumption_user,
            "electricity_cost_user": electricity_cost_user,
            "lowest_price_last_year": lowest_price_kwh,
            "electricity_cost_optimized": electricity_cost_optimized,
            "savings": savings,
            "battery_size": battery
        }

    except Exception as e:
        print("Fehler bei der Berechnung:", e)
        return None

# Beispielaufruf
if __name__ == "__main__":
    result = asyncio.run(calculate_optimized_cost(1234, 0.35, 1200))
    print(result)
