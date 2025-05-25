from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from energyWebapp.general.db.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'mw212_projekt'}

    ID_User = Column(Integer, primary_key=True)
    Username = Column(String(80), unique=True, nullable=False)
    Password = Column(String(200), nullable=False)

    # Beziehung zur ElectricityCost-Tabelle (1:1)
    electricity_cost = relationship(
        "ElectricityCost",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def get_id(self):
        return str(self.ID_User)
