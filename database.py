from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db(create_test_data=False):
    import models
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    if (create_test_data):
        from database import db_session

        eu= models.Region(name='Europe')
        na =models.Region(name='North America')

        db_session.add(eu)
        db_session.add(na)
        
        uk= models.CountryRef(region=eu, name='UK', colour="3e95cd")
        fr= models.CountryRef(region=eu, name='France', colour="8e5ea2")
        us= models.CountryRef(region=na, name='USA', colour="3cba9f")

        db_session.add(uk)
        db_session.add(fr)
        db_session.add(us)

        tpp= models.Metric(name='Total prison population', trends_switch=True, sum_or_ave_switch = True)
        ppr= models.Metric(name='Prison population rate', trends_switch=True, sum_or_ave_switch = False)
        fem = models.Metric(name='Female prisoner %', trends_switch=False, sum_or_ave_switch = False)
        db_session.add(tpp)
        db_session.add(ppr)

        db_session.add(models.CountryData(country=uk, metric=tpp, year = 2018, value=2000 ))
        db_session.add(models.CountryData(country=fr, metric=tpp, year = 2018, value=3000 ))
        db_session.add(models.CountryData(country=us, metric=tpp, year = 2018, value=40000 ))
        db_session.add(models.CountryData(country=uk, metric=tpp, year = 2017, value=2200))
        db_session.add(models.CountryData(country=uk, metric=ppr, year = 2017, value=200))
        db_session.add(models.CountryData(country=uk, metric=ppr, year = 2018, value=150))
        db_session.add(models.CountryData(country=fr, metric=ppr, year = 2018, value=180))
        db_session.add(models.CountryData(country=uk, metric=fem, year = 2018, value=18))
        db_session.add(models.CountryData(country=uk, metric=fem, year = 2017, value=18))

        db_session.commit()