# -*- coding: utf-8 -*-

# pycupbetting

# Copyright (C) <2015> Markus Hackspacher

# This file is part of pycupbetting.

# pycupbetting is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pycupbetting is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pycupbetting.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from sqlalchemy import orm
from sqlalchemy import create_engine
from modules import model


class TestCodeFormat(unittest.TestCase):
    """
    Test of the code format
    """
    def setUp(self):
        """Create an engine and create all the tables we need

        @return:
        """
        engine = create_engine('sqlite:///:memory:', echo=False)
        model.base.metadata.bind = engine
        model.base.metadata.create_all(engine)

        # Set up the session
        sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,
                              expire_on_commit=True)
        self.session = orm.scoped_session(sm)

    def test_user_model(self):
        """Test the user model
        """
        ed_user = model.User(name='ed', fullname='Ed Jones', email='ed@mail')
        self.session.add(ed_user)
        our_user = self.session.query(model.User).filter_by(name='ed').first()
        self.assertEqual(our_user.name, 'ed')
        self.assertEqual(our_user.fullname, 'Ed Jones')
        self.assertEqual(our_user.email, 'ed@mail')

    def test_team_model(self):
        """Test the user model
        """
        teamlist = ['Germany', 'Brasil', 'Italy', 'Spain']
        for te in teamlist:
            self.session.add(model.Team(name=te))
        our_team = self.session.query(model.Team).filter_by(
                name='Germany').first()
        self.assertEqual(our_team.name, 'Germany')
        self.assertEqual(our_team.team_bets, [])
        self.assertEqual(our_team.cup_winner_bets, [])
        self.assertEqual(our_team.competitions, [])
        teams = self.session.query(model.Team).all()
        self.assertEqual(teams[2].name, 'Italy')
        self.assertEqual(teams[3].name, 'Spain')

    def test_competition_model(self):
        """Test the Competition model
        """
        testcompetition = model.Competition(name='World Cup',
                                            cup_winner_id=2,
                                            rule_right_winner=1,
                                            rule_right_goaldif=2,
                                            rule_right_result=3,
                                            rule_cup_winner=10)
        self.session.add(testcompetition)
        our_competition = self.session.query(model.Competition).first()
        self.assertEqual(our_competition.name, 'World Cup')
        self.assertEqual(our_competition.cup_winner_id, 2)
        self.assertEqual(our_competition.rule_right_winner, 1)
        self.assertEqual(our_competition.rule_right_goaldif, 2)
        self.assertEqual(our_competition.rule_right_result, 3)
        self.assertEqual(our_competition.rule_cup_winner, 10)
        self.test_team_model()
        our_competition = self.session.query(model.Competition).first()
        self.assertEqual(our_competition.name, 'World Cup')
        self.assertEqual(our_competition.teams.name, 'Brasil')
