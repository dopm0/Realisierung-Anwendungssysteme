from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, Numeric, String, Date, TIMESTAMP, select, func, cast
from energyWebapp.general.db.extensions import db


class ElectricityPriceHistory(db.Model):
    __tablename__  = 'electricity_price_history'
    __table_args__ = {'schema': 'mw212_projekt'}

    id_electricity_price = Column(Integer, primary_key=True, autoincrement=True)
    timestamp            = Column(TIMESTAMP(timezone=False), nullable=False)
    price_euro           = Column(Numeric(10, 5), nullable=False)


    @classmethod
    def get_prices(cls):
        prices      = cls.query.order_by(cls.timestamp).all()
        timestamps  = [p.timestamp.strftime('%Y-%m-%d %H:%M') for p in prices]
        prices_euro = [float(p.price_euro) for p in prices]
        return {"timestamps": timestamps, "prices_euro": prices_euro}

    @classmethod
    def get_avg_daily_lowest_price_last_year(cls):
        today = datetime.today()
        one_year_ago = today - timedelta(days=365)

        daily_minima_subq = (
            db.session.query(
                cast(func.date(cls.timestamp), Date).label("day"),
                func.min(cls.price_euro).label("daily_min")
            )
            .filter(cls.timestamp.between(one_year_ago, today))
            .group_by(cast(func.date(cls.timestamp), Date))
        ).subquery()

        avg_daily_min = db.session.query(func.avg(daily_minima_subq.c.daily_min)).scalar()

        return float(avg_daily_min)

    @classmethod
    def calculate_optimized_cost(cls, electricity_price_user, electricity_consumption_user, cost_entry):
        network_fees                = 0.12
        lowest_avg_price_mwh        = cls.get_avg_daily_lowest_price_last_year()
        lowest_price_kwh            = lowest_avg_price_mwh / 1000
        electricity_cost_user       = electricity_price_user * electricity_consumption_user
        electricity_cost_optimized  = (lowest_price_kwh + network_fees) * electricity_consumption_user
        savings                     = electricity_cost_user - electricity_cost_optimized
        battery                     = electricity_consumption_user / 365

        cost_entry.electricity_price_user       = electricity_price_user
        cost_entry.electricity_consumption_user = electricity_consumption_user
        cost_entry.electricity_cost_user        = electricity_cost_user
        cost_entry.electricity_cost_optimized   = electricity_cost_optimized
        cost_entry.savings                      = savings
        cost_entry.battery_size                 = battery

        db.session.commit()

        return {
            "electricity_price_user": electricity_price_user,
            "electricity_consumption_user": electricity_consumption_user,
            "electricity_cost_user": electricity_cost_user,
            "electricity_cost_optimized": electricity_cost_optimized,
            "savings": savings,
            "battery_size": battery
        }