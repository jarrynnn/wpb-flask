from sqlalchemy import Column, Integer, String
from database import Base


class Region(Base): 
    id = models.IntegerField(primary_key=True, unique = True)
    name = models.CharField(max_length=200)

    def __repr__(self):
        return self.name
    class Meta:
        ordering = ["name"] 

class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    stat = Column(Integer, nullable=False)
    colour = Column(String(6), nullable=False)
    prev = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    

    def __init__(self, name=None, stat=0, colour="000000", background="000000", prev=0, year =0):
        self.name = name
        self.stat = stat
        self.colour = colour
        self.background = background
        self.prev = prev
        self.year = year

    def __repr__(self):
        return '%r (%s)' % (self.name, self.stat)


def get_country_by_id(id):
    return Country.query.filter(Country.id == id).one_or_none()


def get_country(name):
    return Country.query.filter(Country.name == name).one_or_none()

def get_countries():
    return Country.query.all()