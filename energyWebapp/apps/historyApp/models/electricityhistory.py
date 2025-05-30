from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, Numeric, String, Date, TIMESTAMP, select, func, cast
from energyWebapp.general.db.extensions import db


class ElectricityPriceHistory(db.Model):
    __tablename__  = 'electricity_price_history'
    __table_args__ = {'schema': 'mw212_projekt'}

    id_electricity_price = Column(Integer, primary_key=True, autoincrement=True)
    timestamp            = Column(TIMESTAMP(timezone=False), nullable=False)
    prices_euro          = Column(Numeric(10, 5), nullable=False)


    @classmethod
    def get_prices(cls):
        prices_euro = cls.query.order_by(cls.timestamp).all()
        timestamps  = [p.timestamp.strftime('%Y-%m-%d %H:%M') for p in prices_euro]
        prices_euro      = [float(p.prices_euro) for p in prices_euro]
        return {"timestamps": timestamps, "prices_euro": prices_euro}

    @classmethod
    def get_avg_daily_lowest_price_last_year(cls):
        today = datetime.today()
        one_year_ago = today - timedelta(days=365)

        daily_minima_subq = (
            db.session.query(
                cast(func.date(cls.timestamp), Date).label("day"),
                func.min(cls.prices_euro).label("daily_min")
            )
            .filter(cls.timestamp.between(one_year_ago, today))
            .group_by(cast(func.date(cls.timestamp), Date))
        ).subquery()

        avg_daily_min = db.session.query(func.avg(daily_minima_subq.c.daily_min)).scalar()

        return float(avg_daily_min)
