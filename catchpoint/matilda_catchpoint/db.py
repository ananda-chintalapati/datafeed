from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from matilda_catchpoint import config_reader as cr
from matilda_catchpoint import model

def get_db_string():
    username = cr.get_lookup_data('DATABASE', 'user')
    password = cr.get_lookup_data('DATABASE', 'password')
    host = cr.get_lookup_data('DATABASE', 'host')
    db = cr.get_lookup_data('DATABASE', 'db')
    db_string = 'postgres://' + username + ':' + password + '@' + host + '/' + db
    return db_string

def get_session():
    db = create_engine(get_db_string())
    Session = sessionmaker(db)
    session = Session()
    return session

def get_cp_alerts():
    session = get_session()
    with session.begin():
        query = session.query(model.Catchpoint)
        return query.all()
