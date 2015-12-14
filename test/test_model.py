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
