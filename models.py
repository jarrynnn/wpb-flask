from sqlalchemy import Column, Integer, String
from database import Base

class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    stat = Column(Integer, nullable=False)
    colour = Column(String(6), nullable=False)

    def __init__(self, name=None, stat=0, colour="000000", background="000000"):
        self.name = name
        self.stat = stat
        self.colour = colour
        self.background = background

    def __repr__(self):
        return '%r (%s)' % (self.name, self.stat)

def get_country(name=None):
    return Country.query.filter(Country.name == name).first()

def get_countries():
    return Country.query.all()