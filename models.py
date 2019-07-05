from sqlalchemy import Column, Integer, String, or_
from database import Base

class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    stat = Column(Integer, nullable=False)

    def __init__(self, name=None, stat=0):
        self.name = name
        self.stat = stat

    def __repr__(self):
        return '%r (%s)' % (self.name, self.stat)


def get_countries(name=None):
    return Country.query.filter(or_(Country.name == name, name == None)).all()