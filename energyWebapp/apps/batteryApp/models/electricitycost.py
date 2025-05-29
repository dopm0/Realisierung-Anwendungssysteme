from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from energyWebapp.general.db.extensions import db
from energyWebapp.apps.baseApp.models.electricityhistory import ElectricityPriceHistory


class ElectricityCost(db.Model):
    __tablename__ = 'electricity_cost'
    __table_args__ = {'schema': 'mw212_projekt'}

    id_electricity_cost = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('mw212_projekt.users.ID_User'), nullable=False, unique=True)
    electricity_consumption_user = db.Column(db.Numeric(10, 2))
    electricity_price_user = db.Column(db.Numeric(10, 5))
    electricity_cost_user = db.Column(db.Numeric(12, 2))
    electricity_cost_optimized = db.Column(db.Numeric(12, 2))
    optimized_price = db.Column(db.Numeric(10, 5))
    savings = db.Column(db.Numeric(12, 2))
    battery_size = db.Column(db.Numeric(12, 2))

    user = relationship("User", back_populates="electricity_cost")


    @classmethod
    def calculate_optimized_cost(cls, electricity_price_user, electricity_consumption_user, cost_entry):
        network_fees                = 0.12
        lowest_avg_price_mwh        = ElectricityPriceHistory.get_avg_daily_lowest_price_last_year()
        lowest_avg_price_kwh        = lowest_avg_price_mwh / 1000
        electricity_cost_user       = electricity_price_user * electricity_consumption_user
        electricity_cost_optimized  = (lowest_avg_price_kwh + network_fees) * electricity_consumption_user
        savings                     = electricity_cost_user - electricity_cost_optimized
        battery                     = electricity_consumption_user / 365

        cost_entry.electricity_price_user       = electricity_price_user
        cost_entry.optimized_price              = (lowest_avg_price_kwh + network_fees)
        cost_entry.electricity_consumption_user = electricity_consumption_user
        cost_entry.electricity_cost_user        = electricity_cost_user
        cost_entry.electricity_cost_optimized   = electricity_cost_optimized
        cost_entry.savings                      = savings
        cost_entry.battery_size                 = battery

        db.session.commit()

        return 
