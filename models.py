from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Region(Base): 
    __tablename__ = 'region'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    countries = relationship("CountryRef", back_populates="region") 

    def __repr__(self):
        return self.name

class CountryRef(Base):
    __tablename__ = 'countryref'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    geo_id = Column(String(2), unique=True)     #for map integration (GEOJSON)
    region_id = Column(Integer, ForeignKey('region.id'))
    region = relationship("Region", back_populates="countries")
    name = Column(String(50), unique=True)
    colour = Column(String(6), nullable=False)
    country_datas = relationship("CountryData", back_populates="country") 
    similar_countries = relationship("SimilarCountriesRef", back_populates="selected_country")


class Metric(Base):
    __tablename__ = 'metric'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    trends_switch = Column(Boolean, default=False)
    sum_or_ave_switch = Column(Boolean, default=False)
    country_datas = relationship("CountryData", back_populates="metric")
    


class CountryData(Base):
    __tablename__ = 'country_datas'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    countryref_id = Column(Integer, ForeignKey('countryref.id'))
    country = relationship("CountryRef", back_populates="country_datas")
    metric_id = Column(Integer, ForeignKey('metric.id'))
    metric = relationship("Metric", back_populates="country_datas")
    year = Column(Integer, nullable=False)
    value = Column(Integer, nullable=True)
    exp_value = Column(Integer, nullable=True)

 
    def __repr__(self):
        return '%r %r (%s)' % (self.country, self.metric, self.year)

class SimilarCountriesRef(Base):
    __tablename__ = 'similar_countries'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    selected_countryref_id = Column(Integer, ForeignKey('countryref.id'))
    selected_country = relationship("CountryRef", back_populates="similar_countries")
    country1_id = Column(Integer, nullable=False)
    country2_id = Column(Integer, nullable=False)
    country3_id = Column(Integer, nullable=False)
    country4_id = Column(Integer, nullable=False)
    country5_id = Column(Integer, nullable=False)
    country6_id = Column(Integer, nullable=False)
    country7_id = Column(Integer, nullable=False)
    country8_id = Column(Integer, nullable=False)
    country9_id = Column(Integer, nullable=False)
    country10_id = Column(Integer, nullable=False)



#def get_countrydatas_by_country_id(id):
 #  return CountryData.query.filter(CountryData.countryref_id == id).all()

def get_countrydatas_by_country_id(country_id, metric_id=None, year= None): 
    if metric_id is not None:
        if year is not None: 
            return CountryData.query.filter(CountryData.metric_id == metric_id).filter(CountryData.countryref_id == country_id).filter(CountryData.year == year).all()
        else: 
            return CountryData.query.filter(CountryData.metric_id == metric_id).filter(CountryData.countryref_id == country_id).all()
    else: 
        return CountryData.query.filter(CountryData.countryref_id == country_id).all()

def get_countrydatas():
    return CountryData.query.all()

def get_country_by_id(id):
    return CountryRef.query.filter(CountryRef.id == id).one_or_none()

def get_country(name):
    return CountryRef.query.filter(CountryRef.name == name).one_or_none()

def get_countries():
    return CountryRef.query.all()

def get_metrics():
    return Metric.query.all()

def get_metric_by_id(id):
    return Metric.query.filter(Metric.id == id).one_or_none()