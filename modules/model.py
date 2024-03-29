# -*- coding: utf-8 -*-

"""
pycupbetting

Copyright (C) <2014,2023> Markus Hackspacher

This file is part of pycupbetting.

pycupbetting is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pycupbetting is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU General Public License
along with pycupbetting.  If not, see <http://www.gnu.org/licenses/>.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import registry, relationship

mapper_registry = registry()
Base = mapper_registry.generate_base()

class User(Base):
    """characteristics of the user table"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    email = Column(String)

    cup_winner_bets = relationship("CupWinnerBet",
                                   order_by="CupWinnerBet.id",
                                   backref="users")
    game_bets = relationship("GameBet", order_by="GameBet.id",
                             backref="users")

    def __repr__(self):
        return "<User(name='{0}', fullname='{1}', email='{2}')>".format(
            self.name, self.fullname, self.email)


class Team(Base):
    """characteristics of the team table"""
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    team_bets = relationship("Game", primaryjoin="Game.team_home_id==Team.id"
                             " or Game.team_away_id==Team.id",
                             order_by="Game.id", viewonly=True)
    cup_winner_bets = relationship("CupWinnerBet",
                                   order_by="CupWinnerBet.id",
                                   backref="teams")
    competitions = relationship("Competition", order_by="Competition.id",
                                backref="teams")

    def __repr__(self):
        return "<Team(name='{0}', CupWinnerBet='{1}', competitions='{2}'" \
            " team_bets='{3}'". \
            format(self.name, self.cup_winner_bets, self.competitions,
                   self.team_bets)


class Competition(Base):
    """characteristics of the competition table"""
    __tablename__ = 'competition'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cup_winner_id = Column(Integer, ForeignKey('teams.id'))
    rule_right_winner = Column(Integer)
    rule_right_goaldif = Column(Integer)
    rule_right_result = Column(Integer)
    rule_cup_winner = Column(Integer)

    cup_winner_bets = relationship("CupWinnerBet",
                                   order_by="CupWinnerBet.id",
                                   backref="competition")
    games = relationship("Game", order_by="Game.id", backref="competition")

    def __repr__(self):
        return "<Competition(name='{0}', cup_winner_name='{1}'" \
            " cup_winner_bets='{2}'". \
            format(self.name, self.teams.name, self.cup_winner_bets)


class CupWinnerBet(Base):
    """characteristics of the cup winner bet table"""
    __tablename__ = 'CupWinnerBet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    competition_id = Column(Integer, ForeignKey('competition.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))

    def __repr__(self):
        return "<CupWinnerBet(Username='{0}', competition='{1}'," \
               " team='{2}')>".\
               format(self.users.name, self.competition.name, self.teams.name)

    @property
    def name(self):
        """return CupWinnerBet

        @return:
        """
        return "{0} {1} {2}". \
            format(self.users.name, self.competition.name, self.teams.name)

    @property
    def point(self):
        """CupWinnerBet: points for the right cup winner
        """
        points = 0
        if self.competition.cup_winner_id == self.team_id:
            points = self.games.competition.rule_cup_winner
        return points


class Game(Base):
    """characteristics of the games table
    """
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    competition_id = Column(Integer, ForeignKey('competition.id'))
    team_home_id = Column(Integer, ForeignKey('teams.id'))
    team_away_id = Column(Integer, ForeignKey('teams.id'))
    result_home = Column(Integer)
    result_away = Column(Integer)
    start_date = Column(DateTime, default=datetime.utcnow)

    game_bets = relationship("GameBet", order_by="GameBet.id",
                             backref="games")
    team_home = relationship("Team",
                             primaryjoin="Team.id==Game.team_home_id")
    team_away = relationship("Team",
                             primaryjoin="Team.id==Game.team_away_id")

    def __repr__(self):
        return "<Game(competition='{0}', game='{1}:{2}', result='{3}:{4}'," \
               " bet ='{5}'". \
            format(self.competition.name, self.team_home.name,
                   self.team_away.name, self.result_home, self.result_away,
                   self.game_bets)

    @property
    def name(self):
        """return the game

        @return:
        """
        try:
            team_home_name = self.team_home.name
        except AttributeError:
            team_home_name = "no team home selected"
        try:
            team_away_name = self.team_away.name
        except AttributeError:
            team_away_name = "no team away selected"
        try:
            competition_name = self.competition.name
        except AttributeError:
            competition_name = "no competition selected"

        return "{0}: {1}:{2} {3}:{4}". \
            format(competition_name, team_home_name,
                   team_away_name, self.result_home, self.result_away)


class GameBet(Base):
    """characteristics of the game bet table
    """
    __tablename__ = 'game_bet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    game_id = Column(Integer, ForeignKey('games.id'))
    bet_home = Column(Integer)
    bet_away = Column(Integer)

    def __repr__(self):
        return "<GameBet(name='{0}', competition='{1}', game='{2}:{3}'," \
               "result='{4}:{5}', bet='{6}:{7}'". \
               format(self.users.name,
                      self.games.competition.name,
                      self.games.team_home.name,
                      self.games.team_away.name,
                      self.games.result_home,
                      self.games.result_away,
                      self.bet_home,
                      self.bet_away)

    @property
    def name(self):
        """return the game name and result of the game bet
        """
        return "{0}:{1} {2}:{3}". format(self.games.team_home.name,
                                         self.games.team_away.name,
                                         self.bet_home, self.bet_away)

    @property
    def point(self):
        """Game bet right result, right goaldif and right winner
        """
        points = 0
        if None in (self.games.result_home, self.games.result_away,
                    self.bet_home, self.bet_away):
            return points

        if (self.games.result_home == self.bet_home and
                self.games.result_away == self.bet_away):
            points = self.games.competition.rule_right_result
        elif (self.games.result_home - self.games.result_away ==
              self.bet_home - self.bet_away):
            points = self.games.competition.rule_right_goaldif
        elif ((self.games.result_home > self.games.result_away and
               self.bet_home > self.bet_away) or
              (self.games.result_home < self.games.result_away and
               self.bet_home < self.bet_away)):
            points = self.games.competition.rule_right_winner
        return points
