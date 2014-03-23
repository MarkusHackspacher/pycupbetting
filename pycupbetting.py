#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pycupbetting

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
_ = gettext.gettext

# Create an engine and create all the tables we need
engine = create_engine('sqlite:///dbcupbetting.sqlite', echo=False)
model.Base.metadata.bind = engine
model.Base.metadata.create_all(engine)

# Set up the session
sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=True,
    expire_on_commit=True)
session = orm.scoped_session(sm)


class selection_menu():
    """
    show the selection menu and return the id of table
    """
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


def translation_de():
    """
    set the language
    are more language could be a in parameter
    """
    global _
    lang = gettext.translation("pycupbetting", "locale", languages=['de'])
    _ = lang.gettext


def info():
    print(_('''pycupbetting
        databasestruktur from Markus Hackspacher
        Menu from Christian Hausknecht '''))


def inputpro(in_valve, text):
    """
    Input prozedure
    """
    out_valve = input("{} [{}]:".format(text, in_valve))
    if out_valve == '':
        out_valve = in_valve
    return out_valve


def all_betting(user_id=None, competition_id=None, export=False):
    """
    print all games of competition
    """
    if not competition_id:
        competition_id = int(selection_menu(session.query(
            model.Competition).all()))
    if competition_id == 0:
        return
    comp = session.query(model.Competition).filter_by(
        id=competition_id).one()
    points = 0
    text_winner = ''
    if comp.cup_winner_id:
        text_winner = _("cupwinner: {}\r\n\r\n").format(comp.teams.name)
    if export:
        f = open('games.txt', 'w')
        f.write(_("competition: {} {}\r\n\r\n").format(
            comp.name, text_winner))
    print (_("competition: {} {}").format(
        comp.name, text_winner))
    for cup_winner in comp.cup_winner_bets:
        each_cup_winner = (_('cup winner: {} point:{} ').format(
            cup_winner.teams.name, cup_winner.point))
        if not user_id:
            print (cup_winner.users.name, each_cup_winner,)
            if export:
                f.write(cup_winner.users.name, each_cup_winner)            
        elif cup_winner.user_id == user_id:
            points += cup_winner.point
            print (each_cup_winner)
            if export:
                f.write(each_cup_winner + '\r\n')
    for game in comp.games:
        each_game = (_('game {}').format(game.name))
        print (each_game)
        if export:
            f.write(each_game + '\r\n')
        for bet in game.game_bets:
            each_bet = (_('bet: {}:{} point:{}').format(
                bet.bet_home, bet.bet_away, bet.point))
            if not user_id:
                print (bet.users.name, each_bet)
                if export:
                    f.write(bet.users.name, each_bet + '\r\n')
            elif bet.user_id == user_id :
                points += bet.point
                print (each_bet)
                if export:
                    f.write(each_bet + '\r\n')
    text = (_('points:{}').format(points))
    print (text)
    if export:
        f.write(text + '\r\n')

    if export:
        f.close()


def edit_user(user):
    """
    change of data of table user

    :param user: data
    """
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
    editor_user = functools.partial(edit_user, user)
    new_cup_winner_bet_user = functools.partial(new_cup_winner_bet,
                                                user_id=user.id)
    select_cup_winner_bet_user = functools.partial(select_cup_winner_bet,
                                                   user_id=user.id)
    all_game_bet_user = functools.partial(all_game_bet, user_id=user.id)
    select_game_bet_user = functools.partial(select_game_bet, user_id=user.id)
    all_betting_user = functools.partial(all_betting, user_id=user.id)

    def info_user():
        print (_("user: {} full name: {} email: {}").
           format(user.name, user.fullname, user.email, ))

    userselect = Menu(_("user editor"))
    userselect.textchoice = _('Your choice is ?:')
    userselect.texterror = _('please only enter numbers between 1 and {}')
    userselect.append(_("change user name"), editor_user)
    userselect.append(_("user info"), info_user)
    userselect.append(_("user bettings"), all_betting_user)
    userselect.append(_("add new cup winner bet"), new_cup_winner_bet_user)
    userselect.append(_("cup winner bet selection"),
                        select_cup_winner_bet_user)
    userselect.append(_("edit all game bets"), all_game_bet_user)
    userselect.append(_("game bet selection"), select_game_bet_user)
    userselect.finish()
    userselect.run()


def edit_team(team):
    """
    change of data of table team

    :param team: data
    """
    team.name = inputpro(team.name, _('name of the team'))
    return team


def new_team():
    session.add(edit_team(model.Team()))


def select_team():
    teamid = int(selection_menu(session.query(model.Team).all()))
    if teamid == 0:
        return
    team = session.query(model.Team).filter_by(id=teamid).first()
    editor_team = functools.partial(edit_team, team)

    def info_team():
        print (_("name of the team: {}").format(team.name))

    teamselect = Menu(_("team editor {}").format(team.name))
    teamselect.textchoice = _('Your choice is ?:')
    teamselect.texterror = _('please only enter numbers between 1 and {}')
    teamselect.append(_("change team name"), editor_team)
    teamselect.append(_("team info"), info_team)
    teamselect.finish()
    teamselect.run()


def edit_competition(competition):
    """
    change of data of table competition

    :param competition: data
    """
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


def all_games_competition(competition, export):
    """
    print all games of competition
    """
    if export:
        f = open('games.txt', 'w')
        f.write(_("competition: {}\r\n\r\n").format(competition.name))
    print (_("competition: {}").format(competition.name))
    for game in competition.games:
        each_game = ('{}:{}'.format(game.team_home.name, game.team_away.name))
        print (each_game)
        if export:
            f.write(each_game + '\r\n')
    if export:
        f.close()


def select_competition():
    competitionid = int(selection_menu(session.query(
        model.Competition).all()))
    if competitionid == 0:
        return
    competition = session.query(model.Competition).filter_by(
        id=competitionid).first()
    editor_competition = functools.partial(edit_competition, competition)
    new_game_competition = functools.partial(new_game, competition.id)
    select_game_competition = functools.partial(select_game, competition.id)
    print_all_games_competition = functools.partial(all_games_competition,
                                                    competition, False)
    export_all_games_competition = functools.partial(all_games_competition,
                                                     competition, True)

    def info_competition():
        print (_("competition: {}, Points {},{},{},{}").
               format(competition.name,
               competition.rule_right_winner, competition.rule_right_goaldif,
               competition.rule_right_result, competition.rule_cup_winner,))
        try:
            print (_("cupwinner: {}").format(competition.teams.name))
        except AttributeError:
            print (_("no cupwinner selected"))
    compselect = Menu(_("competition edit menu {}").format(competition.name))
    compselect.textchoice = _('Your choice is ?:')
    compselect.texterror = _('please only enter numbers between 1 and {}')
    compselect.append(_("competition name change"), editor_competition)
    compselect.append(_("competition info"), info_competition)
    compselect.append(_("add game"), new_game_competition)
    compselect.append(_("game selection"), select_game_competition)
    compselect.append(_("show all games"), print_all_games_competition)
    compselect.append(_("export all games"), export_all_games_competition)
    compselect.finish()
    compselect.run()


def edit_cup_winner_bet(cup_winner_bet):
    """
    change of data of table cup_winner_bet

    :param cup_winner_bet: data
    """
    print(_('team selection'))
    cup_winner_bet.team_id = int(selection_menu(
        session.query(model.Team).all()))
    return cup_winner_bet


def new_cup_winner_bet(user_id, competition_id=None):
    """
    :param user_id: data:
    :param competition_id: data
    """
    if not competition_id:
        competition_id = int(selection_menu(session.query(
            model.Competition).all()))
    if competition_id == 0:
        return
    session.add(edit_cup_winner_bet(model.Cup_winner_bet(
        user_id=user_id, competition_id=competition_id)))


def select_cup_winner_bet(user_id, competition_id=None):
    print (user_id)
    if not competition_id:
        competition_id = int(selection_menu(session.query(
            model.Competition).all()))
    if competition_id == 0:
        return
    memberid = int(selection_menu(session.query(
            model.Cup_winner_bet).filter_by(
            user_id=user_id).filter_by(competition_id=competition_id).all()))
    if memberid == 0:
        return
    cup_winner_bet = session.query(model.Cup_winner_bet).filter_by(
        id=memberid).first()
    editor_cup_winner_bet = functools.partial(edit_cup_winner_bet,
                                              cup_winner_bet)

    def delete_cup_winner_bet():
        session.delete(cup_winner_bet)
        return

    cup_winner_betselect = Menu(_("cup winner bet editor {}").format(
        cup_winner_bet.teams.name))
    cup_winner_betselect.textchoice = _('Your choice is ?:')
    cup_winner_betselect.texterror = _(
        'please only enter numbers between 1 and {}')
    cup_winner_betselect.append(_("change cup winner bet"), editor_cup_winner_bet)
    cup_winner_betselect.append(_("delete this bet"), delete_cup_winner_bet)
    cup_winner_betselect.finish()
    cup_winner_betselect.run()


def edit_game(game):
    """
    change of data of table game

    :param game: data
    """
    print(_('team home selection'))
    game.team_home_id = int(selection_menu(
        session.query(model.Team).all()))
    print(_('team away selection'))
    game.team_away_id = int(selection_menu(
        session.query(model.Team).all()))
    game.result_home = inputpro(game.result_home, _('result home'))
    game.result_away = inputpro(game.result_away, _('result away'))
    return game


def new_game(competition_id):
    session.add(edit_game(model.Game(competition_id=competition_id)))


def select_game(competition_id):
    memberid = int(selection_menu(session.query(model.Game).filter_by(
        competition_id=competition_id).all()))
    if memberid == 0:
        return
    game = session.query(model.Game).filter_by(id=memberid).first()
    editor_game = functools.partial(edit_game, game)

    def info_game():
        print (_("name of the competition: {}").format(game.competition.name))
        try:
            print (_("team home: {}").format(game.team_home.name))
        except AttributeError:
            print (_("no team home selected"))
        try:
            print (_("team away: {}").format(game.team_away.name))
        except AttributeError:
            print (_("no team away selected"))

    def delete_game():
        session.delete(game)
        return

    gameselect = Menu(_("game editor"))
    gameselect.textchoice = _('Your choice is ?:')
    gameselect.texterror = _('please only enter numbers between 1 and {}')
    gameselect.append(_("change game"), editor_game)
    gameselect.append(_("team info"), info_game)
    gameselect.append(_("delete this game"), delete_game)
    gameselect.finish()
    gameselect.run()


def edit_game_bet(game_bet):
    """
    change of data of table game_bet

    :param game_bet: data
    """
    game_bet.bet_home = inputpro(game_bet.bet_home, _('bet result home'))
    game_bet.bet_away = inputpro(game_bet.bet_away, _('bet result away'))

    return game_bet


def all_game_bet(user_id=None, competition_id=None):
    """
    :param user_id: data:
    :param competition_id: data
    """
    if not user_id:
        user_id = int(selection_menu(session.query(
            model.User).all()))
    if user_id == 0:
        return
    if not competition_id:
        competition_id = int(selection_menu(session.query(
            model.Competition).all()))
    if competition_id == 0:
        return
    for games in session.query(model.Game).filter_by(
            competition_id=competition_id).all():
        print (games.name)
        game_bets = session.query(model.Game_bet).filter_by(
            user_id=user_id).filter_by(game_id=games.id).all()
        if game_bets:
            print ('you have bet')
            for game_bet in game_bets:
                print (game_bet.name)
                edit_game_bet(game_bet)
        else:
            print ('not bet')
            session.add(edit_game_bet(model.Game_bet(user_id=user_id,
                                                     game_id=games.id)))


def select_game_bet(user_id=None, game_id=None):
    if not user_id:
        user_id = int(selection_menu(session.query(
            model.User).all()))
    if user_id == 0:
        return
    if not game_id:
        game_id = int(selection_menu(session.query(
            model.Game).all()))
    if game_id == 0:
        return
    memberid = int(selection_menu(session.query(model.Game_bet).filter_by(
            user_id=user_id).filter_by(game_id=game_id).all()))
    if memberid == 0:
        return
    game_bet = session.query(model.Game_bet).filter_by(id=memberid).first()
    editor_game_bet = functools.partial(edit_game_bet, game_bet)

    def info_game_bet():
        print (_("info of the game bet: {}").format(game_bet.name))

    def delete_game_bet():
        session.delete(game_bet)
        return

    game_betselect = Menu(_("game bet editor {}").format(game_bet.name))
    game_betselect.textchoice = _('Your choice is ?:')
    game_betselect.texterror = _('please only enter numbers between 1 and {}')
    game_betselect.append(_("change game bet"), editor_game_bet)
    game_betselect.append(_("gamebet info"), info_game_bet)
    game_betselect.append(_("delete this bet"), delete_game_bet)
    game_betselect.finish()
    game_betselect.run()


def main():
    """
    main of pycupbetting
    show the mainmenu
    """
    menu = Menu(_("mainmenu"))
    menu.textchoice = _('Your choice is ?:')
    menu.texterror = _('please only enter numbers between 1 and {}')
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

    menu.append(_("all betting"), all_betting)
    menu.append_submenu(teamsub)
    menu.append_submenu(usersub)
    menu.append_submenu(competitionsub)

    # create 'Exit'-entries automatically - nice to have this :-)
    # saves a lot of typing... :-)))
    menu.finish(text=_("exit"))

    # shake it!
    menu.run()

if __name__ == "__main__":
    languagemenu = Menu("language")
    languagemenu.append("Deutsch", translation_de)
    languagemenu.finish(text="english")
    languagemenu.run(once=True)
    main()
