#!/usr/bin/env python
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

testteam = model.Team(name='Germany')
session.add(testteam)

testcompetition = model.Competition(name='World Cup 2014')
session.add(testcompetition)

ed_winner = model.Cup_winner_bet(competition_id= 1, team_id=1, user_id=1)
session.add(ed_winner)
session.commit()

our_user = session.query(model.User).filter_by(name='ed').first() 
print our_user
print our_user.cup_winner_bets
our_winner = session.query(model.Cup_winner_bet).filter_by(user_id=our_user.id).first() 
print our_winner

