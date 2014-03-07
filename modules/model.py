# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, backref

# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    email = Column(String)
    password_hash = Column(String)

    cup_winner_bets = relationship("Cup_winner_bet", order_by="Cup_winner_bet.id", backref="users")
    game_bets = relationship("Game_bet", order_by="Game_bet.id", backref="users")

    def __repr__(self):
        return "<User(name='%s', fullname='%s', email='%s')>" % (
                                self.name, self.fullname, self.email)

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    cup_winner_bets = relationship("Cup_winner_bet", order_by="Cup_winner_bet.id", backref="teams")    
    #games = relationship("Game", order_by="Game.id", backref="teams")    

class Competition(Base):
    __tablename__ = 'competition'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cup_winner = Column(Integer, ForeignKey('teams.id'))
    rule_right_winner = Column(Integer)
    rule_right_goaldif = Column(Integer)
    rule_right_result = Column(Integer)
    rule_cup_winner = Column(Integer)

    cup_winner_bets = relationship("Cup_winner_bet", order_by="Cup_winner_bet.id", backref="competition")    

class Cup_winner_bet(Base):
    __tablename__ = 'cup_winner_bet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    competition_id = Column(Integer, ForeignKey('competition.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))

    def __repr__(self):
        return "<Cup_winner_bet(Username='%s', competition='%s', team='%s')>" % (
                                self.users.name, self.competition.name, self.teams.name)
class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    competition_id = Column(Integer, ForeignKey('competition.id'))
    team_a_id = Column(Integer, ForeignKey('teams.id'))
    team_b_id = Column(Integer, ForeignKey('teams.id'))
    result_a = Column(Integer)
    result_b = Column(Integer)
    start_date = Column(Date)


class Game_bet(Base):
    __tablename__ = 'game_bet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    game_id = Column(Integer, ForeignKey('games.id'))
    bet_a = Column(Integer)
    bet_b = Column(Integer)
