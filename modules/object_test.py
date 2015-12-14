#!/usr/bin/env python
# -*- coding: utf-8 -*-

import model
from sqlalchemy import orm
from sqlalchemy import create_engine

# Create an engine and create all the tables we need
engine = create_engine('sqlite:///:memory:', echo=False)
model.base.metadata.bind = engine
model.base.metadata.create_all(engine)

# Set up the session
sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,
                      expire_on_commit=True)
session = orm.scoped_session(sm)

ed_user = model.User(name='ed', fullname='Ed Jones', email='ed@mail')
session.add(ed_user)

teamlist = ['Germany', 'Brasil', 'Italy', 'Spain']
for te in teamlist:
    session.add(model.Team(name=te))

testcompetition = model.Competition(name='World Cup 2014', cup_winner_id=2,
                                    rule_right_goaldif=2, rule_right_result=3)
session.add(testcompetition)

ed_winner = model.Cup_winner_bet(competition_id=1, team_id=1, user_id=1)
session.add(ed_winner)

session.commit()

our_user = session.query(model.User).filter_by(name='ed').first()
print our_user
print our_user.cup_winner_bets
our_winner = session.query(
    model.Cup_winner_bet).filter_by(user_id=our_user.id).first()
print our_winner
teams = session.query(model.Team).all()
print teams

gametest = model.Game(competition_id=1, team_home_id=2, team_away_id=3,
                      result_home=2, result_away=2)
session.add(gametest)
gametest = model.Game(competition_id=1, team_home_id=2, team_away_id=1,
                      result_home=1, result_away=2)
session.add(gametest)
gamebettest = model.Game_bet(user_id=1, game_id=1, bet_home=1, bet_away=1)
session.add(gamebettest)
session.commit()
gamebettest = model.Game_bet(user_id=1, game_id=2, bet_home=1, bet_away=2)
session.add(gamebettest)
our_user = session.query(model.User).filter_by(name='ed').first()
print our_user
print our_user.game_bets
our_bet = session.query(model.Game_bet).all()
print sum(x.point for x in our_bet)


def edit_user(user):
    default = user.name
    try:
        user.name = raw_input("user name [{}]:".format(default))
    except SyntaxError:
        user.name = default
    return user
# print name
our_user = edit_user(our_user)
print our_user.name
session.add(edit_user(model.User()))

all_user = session.query(model.User).all()
print all_user
