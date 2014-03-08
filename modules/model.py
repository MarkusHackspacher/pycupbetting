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
    competitions = relationship("Competition", order_by="Competition.id", backref="teams")    

    def __repr__(self):
        return "<Team(name='{}', cup_winner_bets='{}', competitions='{}'". \
            format(self.name, self.cup_winner_bets, self.competitions)

class Competition(Base):
    __tablename__ = 'competition'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cup_winner_id = Column(Integer, ForeignKey('teams.id'))
    rule_right_winner = Column(Integer)
    rule_right_goaldif = Column(Integer)
    rule_right_result = Column(Integer)
    rule_cup_winner = Column(Integer)

    cup_winner_bets = relationship("Cup_winner_bet", order_by="Cup_winner_bet.id", backref="competition")    
    games = relationship("Game", order_by="Game.id", backref="competition")    

    def __repr__(self):
        return "<Competition(name='{}', cup_winner_name='{}' cup_winner_bets='{}'". \
            format(self.name, self.teams.name, self.cup_winner_bets)

class Cup_winner_bet(Base):
    __tablename__ = 'cup_winner_bet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    competition_id = Column(Integer, ForeignKey('competition.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))

    def __repr__(self):
        return "<Cup_winner_bet(Username='%s', competition='%s', team='%s')>" % (
                                self.users.name, self.competition.name, self.teams.name)

    @property
    def point(self):
        points = 0
        if self.competition.cup_winner_id == self.team_id:
                points =  self.games.competition.rule_cup_winner
                print ("Cup_winner_bet: right cup_winner")
	return points

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    competition_id = Column(Integer, ForeignKey('competition.id'))
    team_home_id = Column(Integer, ForeignKey('teams.id'))
    team_away_id = Column(Integer, ForeignKey('teams.id'))
    result_home = Column(Integer)
    result_away = Column(Integer)
    start_date = Column(Date)

    game_bets = relationship("Game_bet", order_by="Game_bet.id", backref="games")    
    team_home = relationship("Team",
                primaryjoin="Team.id==Game.team_home_id")
    team_away = relationship("Team",
                primaryjoin="Team.id==Game.team_away_id")

    def __repr__(self):
        return "<Game(competition='{}', game='{}:{}', result='{}:{}', bet ='{}'". \
            format(self.competition.name, self.team_home.name, self.team_away.name,
                   self.result_home, self.result_away, self.game_bets)

class Game_bet(Base):
    __tablename__ = 'game_bet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    game_id = Column(Integer, ForeignKey('games.id'))
    bet_home = Column(Integer)
    bet_away = Column(Integer)

    def __repr__(self):
        return "<Game_bet(name='{}', competition='{}', game='{}:{}', result='{}:{}', bet='{}:{}'". \
            format(self.users.name, self.games.competition.name, self.games.team_home.name,
             self.games.team_away.name, self.games.result_home, self.games.result_away,
             self.bet_home, self.bet_away)

    @property
    def point(self):
        points = 0
        if (self.games.result_home ==  self.bet_home and
            self.games.result_away ==  self.bet_away):
                points =  self.games.competition.rule_right_result
                print ("Game_bet: right result")
        elif (self.games.result_home - self.games.result_away ==
            self.bet_home - self.bet_away):
                points =  self.games.competition.rule_right_goaldif        
                print ("Game_bet: right goaldif")
        elif ((self.games.result_home > self.games.result_away and
            self.bet_home > self.bet_away) or
            (self.games.result_home < self.games.result_away and
            self.bet_home < self.bet_away)):
                points =  self.games.competition.rule_right_winner        
                print ("Game_bet: right winner")
        return points