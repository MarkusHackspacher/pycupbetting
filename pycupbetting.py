#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pycupbetting, load module lotto

Copyright (C) <2014> Markus Hackspacher

This file is part of pycupbetting.

pyLottoverwaltung is free software: you can redistribute it and/or modify
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

from modules import model
from sqlalchemy import orm
from sqlalchemy import create_engine
import functools

from classymenu import Menu

# Create an engine and create all the tables we need
engine = create_engine('sqlite:///dbcupbetting.sqlite', echo=False)
model.Base.metadata.bind = engine
model.Base.metadata.create_all(engine)

# Set up the session
sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=True,
    expire_on_commit=True)
session = orm.scoped_session(sm)


class selection_menu():
    def __init__(self, datatable):
        self.selection_id = 0
        select = Menu("Auswahlmenü")
        for entry in datatable:
            get_id = functools.partial(self.get_id, entry.id)
            select.append(entry.name, get_id)
        select.finish(text="Zurück")
        select.run(once=True)

    def __int__(self):
        return self.selection_id

    def get_id(self, number):
        self.selection_id = number


def info():
    print('''pycupbetting Programminfos
        Datenbankstruktur von Markus Hackspacher
        Menü von Christian Hausknecht ''')


def edit_user(user):
    default = user.name
    user.name = input("Benuzername [{}]:".format(default))
    if user.name == '':
        user.name = default
    default = user.fullname
    user.fullname = input("Voller Name [{}]:".format(default))
    if user.fullname == '':
        user.fullname = default
    default = user.email
    user.email = input("Email [{}]:".format(default))
    if user.email == '':
        user.email = default
    return user


def new_user():
    session.add(edit_user(model.User()))


def select_user():
    userid = int(selection_menu(session.query(model.User).all()))
    if userid == 0:
        return
    user = session.query(model.User).filter_by(id=userid).first()

    def editor_user():
        edit_user(user)

    def info_user():
        print ("Username: {} Vollername: {} Email: {}".
           format(user.name, user.fullname, user.email, ))

    userselect = Menu("Usereditormenü")
    userselect.append("Usernamen ändern", editor_user)
    userselect.append("Userinfo", info_user)
    userselect.finish()
    userselect.run()


def edit_team(team):
    default = team.name
    team.name = input("Team Name [{}]:".format(default))
    if team.name == '':
        team.name = default
    return team


def new_team():
    session.add(edit_team(model.Team()))


def select_team():
    teamid = int(selection_menu(session.query(model.Team).all()))
    if teamid == 0:
        return
    team = session.query(model.Team).filter_by(id=teamid).first()

    def editor_team():
        edit_team(team)

    def info_team():
        print ("Teamname: {}".format(team.name))

    teamselect = Menu("Teameditormenü {}".format(team.name))
    teamselect.append("Teamnamen ändern", editor_team)
    teamselect.append("Teaminfo", info_team)
    teamselect.finish()
    teamselect.run()


def main():
    menu = Menu("Hauptmenü")
    menu.append("Info", info)

    teamsub = Menu("Teammenü")
    teamsub.append("Team hinzufügen", new_team)
    teamsub.append("Team auswählen", select_team)

    usersub = Menu("Usermenü")
    usersub.append("User hinzufügen", new_user)
    usersub.append("User auswählen", select_user)

    #competitionsub = Menu("Wettbewerb")
    #competitionsub.append("Wettbewerb hinzufügen", new_competition)
    #competitionsub.append("Wettbewerb auswählen", select_competition)

    menu.append_submenu(teamsub)
    menu.append_submenu(usersub)

    # create 'Exit'-entries automatically - nice to have this :-)
    # saves a lot of typing... :-)))
    menu.finish()

    # shake it!
    menu.run()

if __name__ == "__main__":
    main()
