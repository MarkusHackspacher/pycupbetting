# -*- coding: utf-8 -*-

import model
from sqlalchemy import orm
from sqlalchemy import create_engine

# Create an engine and create all the tables we need
engine = create_engine('sqlite:///:memory:', echo=True)
model.Base.metadata.bind = engine
model.Base.metadata.create_all(engine) 

# Set up the session
sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,
    expire_on_commit=True)
session = orm.scoped_session(sm)

ed_user = model.User(name='ed', fullname='Ed Jones', email='ed@mail')
session.add(ed_user)

our_user = session.query(model.User).filter_by(name='ed').first() 
print our_user
session.commit()
print our_user.cup_winner_bets
