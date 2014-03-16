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

import gettext
trans = gettext.translation("pycupbetting", "locale", languages=['de']) 
trans.install()

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
        select = Menu(_("selection"))
        for entry in datatable:
            get_id = functools.partial(self.get_id, entry.id)
            select.append(entry.name, get_id)
        select.finish(text=_("back"))
        select.run(once=True)

    def __int__(self):
        return self.selection_id

    def get_id(self, number):
        self.selection_id = number


def info():
    print(_('''pycupbetting
        databasestruktur from Markus Hackspacher
        Menu from Christian Hausknecht '''))


def inputpro(in_valve, text):
    out_valve = input("{} [{}]:".format(text, in_valve))
    if out_valve == '':
        out_valve = in_valve
    return out_valve


def edit_user(user):
    user.name = inputpro(user.name, _('short user name'))
    user.fullname = inputpro(user.fullname, _('full name'))
    user.email = inputpro(user.email, _('email'))
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
        print (_("user: {} full name: {} email: {}").
           format(user.name, user.fullname, user.email, ))

    userselect = Menu(_("user editor"))
    userselect.append(_("change user name"), editor_user)
    userselect.append(_("user info"), info_user)
    userselect.finish()
    userselect.run()


def edit_team(team):
    team.name = inputpro(team.name, _('name of the team'))
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
        print (_("name of the team: {}").format(team.name))

    teamselect = Menu(_("team editor {}").format(team.name))
    teamselect.append(_("change team name"), editor_team)
    teamselect.append(_("team info"), info_team)
    teamselect.finish()
    teamselect.run()


def edit_competition(competition):
    competition.name = inputpro(competition.name, _('name of competition'))
    competition.rule_right_winner = int(inputpro(
        competition.rule_right_winner, _('points for right winner')))
    competition.rule_right_goaldif = int(inputpro(
        competition.rule_right_goaldif, _('points for right goaldif')))
    competition.rule_right_result = int(inputpro(
        competition.rule_right_result, _('points for right result')))
    competition.rule_cup_winner = int(inputpro(
        competition.rule_cup_winner, _('point for right cup winner')))
    print(_('cup winner selection'))
    competition.cup_winner_id = int(selection_menu(
        session.query(model.Team).all()))
    return competition


def new_competition():
    session.add(edit_competition(model.Competition()))


def select_competition():
    competitionid = int(selection_menu(session.query(
        model.Competition).all()))
    if competitionid == 0:
        return
    competition = session.query(model.Competition).filter_by(
        id=competitionid).first()

    def editor_competition():
        edit_competition(competition)

    def info_competition():
        print (_("competition: {}").format(competition.name))

    teamselect = Menu(_("competition edit menu {}").format(competition.name))
    teamselect.append(_("competition name change"), editor_competition)
    teamselect.append(_("competition info"), info_competition)
    teamselect.finish()
    teamselect.run()


def main():
    menu = Menu(_("mainmenu"))
    menu.append(_("info"), info)

    teamsub = Menu(_("team menu"))
    teamsub.append(_("add team"), new_team)
    teamsub.append(_("team selection"), select_team)

    usersub = Menu(_("user menu"))
    usersub.append(_("add user"), new_user)
    usersub.append(_("user selection"), select_user)

    competitionsub = Menu(_("competition menu"))
    competitionsub.append(_("add competition"), new_competition)
    competitionsub.append(_("competition selection"), select_competition)

    gamesub = Menu(_("game"))
    #gamesub.append(_("add game"), new_game)
    #gamesub.append(_("game selection"), select_game)
    game_betsub = Menu(_("game bet"))
    #game_betsub.append(_("add game bet"), new_game_betsub)
    #game_betsub.append(_("game bet selection"), select_game_betsub)
    cup_winner_betsub = Menu(_("cup winner bet"))
    #cup_winner_betsub.append(_("add cup winner bet"),
    # new_cup_winner_betsub)
    #cup_winner_betsub.append(_("cup winner bet selection"),
    # select_cup_winner_betsub)
    menu.append_submenu(teamsub)
    menu.append_submenu(usersub)
    menu.append_submenu(competitionsub)
    menu.append_submenu(gamesub)
    menu.append_submenu(game_betsub)
    menu.append_submenu(cup_winner_betsub)

    # create 'Exit'-entries automatically - nice to have this :-)
    # saves a lot of typing... :-)))
    menu.finish(text=_("exit"))

    # shake it!
    menu.run()

if __name__ == "__main__":
    main()
