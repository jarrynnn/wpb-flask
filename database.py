from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db(create_test_data=False):
    import models

    Base.metadata.create_all(bind=engine)

    if (create_test_data):
        from database import db_session

        db_session.add(models.Country(name='UK', stat=100))
        db_session.add(models.Country(name='China', stat=17))
        db_session.add(models.Country(name='USA', stat=198))

        db_session.commit()