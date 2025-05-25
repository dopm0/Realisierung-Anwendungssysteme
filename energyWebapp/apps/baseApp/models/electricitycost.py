from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from energyWebapp.general.db.extensions import db

class ElectricityCost(db.Model):
    __tablename__ = 'electricity_cost'
    __table_args__ = {'schema': 'mw212_projekt'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('mw212_projekt.users.ID_User'), nullable=False, unique=True)
    electricity_consumption_user = db.Column(db.Numeric(10, 2))
    electricity_price_user = db.Column(db.Numeric(10, 5))
    electricity_cost_user = db.Column(db.Numeric(12, 2))
    electricity_cost_optimized = db.Column(db.Numeric(12, 2))
    savings = db.Column(db.Numeric(12, 2))
    battery_size = db.Column(db.Numeric(12, 2))

    user = relationship("User", back_populates="electricity_cost")
