from sqlalchemy import Column, Integer, String, Date, ForeignKey

# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    email = Column(String)
    password_hash = Column(String)

class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Competition(Base):
    __tablename__ = 'competition'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cup_winner = Column(Integer)
    rule_right_winner = Column(Integer)
    rule_right_goaldif = Column(Integer)
    rule_right_result = Column(Integer)
    rule_cup_winner = Column(Integer)

class Cup_winner_bet(Base):
    __tablename__ = 'cup_winner_bet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    competition_id = Column(Integer, ForeignKey('competition.id'))
    team_id = Column(Integer, ForeignKey('team.id'))

class Game(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    competition_id = Column(Integer, ForeignKey('competition.id'))
    team_a_id = Column(Integer, ForeignKey('team.id'))
    team_b_id = Column(Integer, ForeignKey('team.id'))
    result_a = Column(Integer)
    result_b = Column(Integer)
    start_date = Column(Date)

class Game_bet(Base):
    __tablename__ = 'game_bet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    game_id = Column(Integer, ForeignKey('game.id'))
    bet_a = Column(Integer)
    bet_b = Column(Integer)
