#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
pycupbetting

Copyright (C) <2014-2023> Markus Hackspacher

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
from sqlalchemy import orm, literal,  create_engine
import functools
import json
import gettext
import glob

from modules import model
from modules.classymenu import Menu

_ = gettext.gettext

# Create an engine and create all the tables we need
engine = create_engine('sqlite:///dbcupbetting.sqlite', echo=False)
model.Base.metadata.bind = engine
model.Base.metadata.create_all(engine)

# Set up the session
sm = orm.sessionmaker(bind=engine,
                      autoflush=True,
                      autocommit=True,
                      expire_on_commit=True)
session = orm.scoped_session(sm)


class SelectionMenu(object):
    """
    show the selection menu and return the id of table
    """
    def __init__(self, datatable, finishtext=_("back")):
        """
        initialisation, datatable is from the database with .name and .id field
        with the variable finishtext change the test at the end
        of the selection, maybe 'None' for no choise

        :type datatable: datatable
        :param datatable: datatable from the database
        :type finishtext: string
        :param finishtext: text of the finish
        """
        self.datatable = datatable
        self.finishtext = finishtext
        self.selection_id = 0
        self.select = Menu(_("selection"))
        self.select.textchoice = _('Your choice is ?:')
        self.select.texterror = _('please only enter numbers between 1 and {}')

    def printdata(self):
        """
        prepare the datatable
        """
        for entry in self.datatable:
            get_id = functools.partial(self.get_id, entry.id)
            self.select.append(entry.name, get_id)
        self.select.finish(text=self.finishtext)
        self.select.run(once=True)

    def get_id(self, number):
        """
        assign database table id
        :type number: int
        :param number: number of item
        """
        self.selection_id = number

    def __int__(self):
        """
        print data table and give id back
        """
        self.printdata()
        return self.selection_id


def translation_de():
    """
    set the german language
    """
    global _
    lang = gettext.translation("pycupbetting", "locale", languages=['de'])
    _ = lang.gettext


def translation_eo():
    """
    set the language
    """
    global _
    lang = gettext.translation("pycupbetting", "locale", languages=['eo'])
    _ = lang.gettext


def info():
    """
    show info text
    """
    print(_('''pycupbetting
        databasestruktur by Markus Hackspacher
        Menu by Christian Hausknecht

        add teams, add competion, add game in competion
        add user, add user bettings
        add game results and enjoy'''))


def inputpro(in_data, text):
    """
    Input procedure for string

    :type in_data: string
    :param in_data: default worth
    :type text: string
    :param text: query text

    :rtype: string
    :return: input worth
    """
    out_data = input("{0} [{1}]:".format(text, in_data))
    if out_data == '':
        out_data = in_data
    return out_data


def inputint(in_data, text):
    """
    Input procedure for integer

    :type in_data: int
    :param in_data: default worth
    :type text: string
    :param text: query text

    :rtype: int
    :return: input worth
    """
    if in_data:
        questiontext = "{0} [{1}]:".format(text, in_data)
    else:
        questiontext = "{}:".format(text)
    while True:
        try:
            data = input(questiontext)
            if data == '' and in_data:
                return in_data
            out_data = int(data)
            return out_data
        except (ValueError):
            print(_('Please enter a number'))


def importJsonUserBet():
    """add a json table with user bet games

    the file table: competition=competition.name,
    Name='', Email='', Winnerbet='', games
    games{game_a,game_b,tip_a='None',tip_b='None'))
    :return:
    """
    jsonfiles = glob.glob('*.txt')
    for filelist in enumerate(jsonfiles):
        print(_("Enter {} for {}").format(filelist[0], filelist[1]))
    try:
        filenr = int(input())
    except ValueError:
        print(_('Enter a number'))
        return
    with open(jsonfiles[filenr], "r") as json_data:
        data = json.load(json_data)

    q = session.query(model.User).filter(
        model.User.name == data['Name'])
    if session.query(literal(True)).filter(q.exists()).scalar():
        print(_('{} already exist').format(data['Name']))
    else:
        session.add(model.User(
            name=data['Name'],
            fullname=data['Name'],
            email=data['Email']))
    q = session.query(model.Competition).filter(
        model.Competition.name == data['competition'])
    if not data['competition'] or not session.query(literal(True)).filter(q.exists()).scalar():
        competition_id = int(SelectionMenu(session.query(
            model.Competition).all()))
        if competition_id == 0:
            return
    else:
        competition_id = session.query(model.Competition).filter_by(
            name=data['competition']).one().id
    user_id = session.query(model.User).filter_by(
        name=data['Name']).one().id
    for bets in data['games']:
        team_home_id = session.query(model.Team).filter_by(
            name=bets['game_a']).one().id
        team_away_id = session.query(model.Team).filter_by(
            name=bets['game_b']).one().id
        game_id = session.query(model.Game).filter_by(
            competition_id=competition_id).filter_by(
            team_home_id=team_home_id).filter_by(
            team_away_id=team_away_id).one().id

        q = session.query(model.GameBet).filter(
            model.GameBet.user_id == user_id).filter(
            model.GameBet.game_id == game_id)
        if session.query(literal(True)).filter(q.exists()).scalar():
            print(_('{} already exist').format(game_id))
        else:
            session.add(model.GameBet(user_id=user_id,
                                      game_id=game_id,
                                      bet_home=bets['tip_a'],
                                      bet_away=bets['tip_b']))
    Winnerbet_id = session.query(model.Team).filter_by(
        name=data['Winnerbet']).one().id

    q = session.query(model.CupWinnerBet).filter(
        model.CupWinnerBet.user_id == user_id).filter(
        model.CupWinnerBet.competition_id == competition_id)
    if session.query(literal(True)).filter(q.exists()).scalar():
        print(_('{} already exist').format(competition_id))
    else:
        session.add(model.CupWinnerBet(user_id=user_id,
                                       competition_id=competition_id,
                                       team_id=Winnerbet_id))


def add_json():
    """add a json table with cup games

    :return:
    """
    jsonfiles = glob.glob('*.json')
    for filelist in enumerate(jsonfiles):
        print(_("Enter {} for {}").format(filelist[0], filelist[1]))
    try:
        filenr = int(input())
    except ValueError:
        print(_('Enter a number'))
        return
    with open(jsonfiles[filenr], "r") as json_data:
        data = json.load(json_data)
    print(data['competition'])
    q = session.query(model.Competition).filter(
        model.Competition.name == data['competition'])
    if session.query(literal(True)).filter(q.exists()).scalar():
        print(_('competition already exist'))
        return
    session.add(model.Competition(
        name=data['competition'],
        rule_right_winner=data['rule_right_winner'],
        rule_right_goaldif=data['rule_right_goaldif'],
        rule_right_result=data['rule_right_result'],
        rule_cup_winner=data['rule_cup_winner']))
    competition_id = session.query(model.Competition).filter_by(
        name=data['competition']).one().id
    for group in data['groups']:
        team_id = []
        for team in group['teams']:
            q = session.query(model.Team).filter(model.Team.name == team)
            if not session.query(literal(True)).filter(q.exists()).scalar():
                session.add(model.Team(name=team))
            team_id.append(session.query(model.Team).filter_by(
                name=team).one().id)
        for pairing in group['pairings']:
            try:
                starttime = pairing[2]
            except IndexError:
                starttime = datetime.now()
            session.add(model.Game(
                competition_id=competition_id,
                team_home_id=team_id[pairing[0]],
                team_away_id=team_id[pairing[1]],
                start_date=starttime))


def all_betting(user_id=None, competition_id=None, export=False):
    """
    print all games of competition
    """
    if not competition_id:
        competition_id = int(SelectionMenu(session.query(
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
        f = open('all.csv', 'w')
    for game in comp.games:
        each_game = _('game {} ').format(game.name)
        print(each_game)
        if export:
            f.write(each_game + _(','))
        for bet in game.game_bets:
            each_bet = _('bet: {}:{} point:{}').format(
                bet.bet_home, bet.bet_away, bet.point)
            if not user_id:
                print(bet.users.name, each_bet)
                if export:
                    f.write(bet.users.name + _(',') + each_bet + _(','))
            elif bet.user_id == user_id:
                points += bet.point
                print(each_bet)
                if export:
                    f.write(each_bet + '\r\n')
        if export:
            f.write('\r\n')
    print(_("competition: {} {}").format(
        comp.name, text_winner))
    if export:
        f.write(text_winner + _(','))
    for cup_winner in comp.cup_winner_bets:
        each_cup_winner = _('cup winner: {} point:{}').format(
            cup_winner.teams.name, cup_winner.point) + _(',')
        if not user_id:
            print(cup_winner.users.name, each_cup_winner,)
            if export:
                f.write(cup_winner.users.name + _(',') + each_cup_winner)
        elif cup_winner.user_id == user_id:
            points += cup_winner.point
            print(each_cup_winner)
            if export:
                f.write(each_cup_winner + _(','))
    if export:
        f.write('\r\n')
        f.write(_(','))
    for cup_winner in comp.cup_winner_bets:
        each_cup_winner = _('all points:{}').format(
            sum(x.point for x in cup_winner.users.game_bets) +
            cup_winner.point) + _(',')
        print(each_cup_winner)
        if export:
            f.write(_(',') + each_cup_winner)

    if export:
        f.close()


def edit_user(user):
    """
    change of data of table user

    :type user: user
    :param user: data of the user
    """
    user.name = inputpro(user.name, _('short user name'))
    user.fullname = inputpro(user.fullname, _('full name'))
    user.email = inputpro(user.email, _('email'))
    return user


def new_user():
    """add a new user

    :return:
    """
    session.add(edit_user(model.User()))


def info_user(user):
    """return info of a user

    :param user:
    :return:
    """
    print(_("user: {} full name: {} email: {}").
          format(user.name, user.fullname, user.email, ))


def select_user():
    """select a user

    :return:
    """
    userid = int(SelectionMenu(session.query(model.User).all()))
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
    info_user_select = functools.partial(info_user, user)

    userselect = Menu(_("user editor"))
    userselect.textchoice = _('Your choice is ?:')
    userselect.texterror = _('please only enter numbers between 1 and {}')
    userselect.append(_("change user name"), editor_user)
    userselect.append(_("user info"), info_user_select)
    userselect.append(_("user bettings"), all_betting_user)
    userselect.append(_("add new cup winner bet"), new_cup_winner_bet_user)
    userselect.append(_("cup winner bet selection"),
                      select_cup_winner_bet_user)
    userselect.append(_("edit all game bets"), all_game_bet_user)
    userselect.append(_("game bet selection"), select_game_bet_user)
    userselect.finish(text=_("back"))
    userselect.run()


def edit_team(team):
    """
    change of data of table team

    :type team: team
    :param team: data
    """
    team.name = inputpro(team.name, _('name of the team'))
    return team


def new_team():
    """add a new team

    :return:
    """
    session.add(edit_team(model.Team()))


def info_team(team):
    """return info of a team

    :param team:
    :return:
    """
    print(_("name of the team: {}").format(team.name))
    print(_("winner of competitions: {}").format(
        "".join(_.name for _ in team.competitions)))
    print(_("bet of winner at competitions: {}").format(
        "".join(_.name for _ in team.cup_winner_bets)))
    print(_("bet of games: {}").format(
        "".join(_.name for _ in team.team_bets)))


def select_team():
    """select a team

    :return:
    """
    teamid = int(SelectionMenu(session.query(model.Team).all()))
    if teamid == 0:
        return
    team = session.query(model.Team).filter_by(id=teamid).first()
    editor_team = functools.partial(edit_team, team)
    info_team_sel = functools.partial(info_team, team)

    def delete_team():
        if (team.cup_winner_bets == [] and team.competitions == [] and
                team.team_bets == []):
            print(_("team {} is deleted").format(team.name))
            session.delete(team)
            teamselect.menushow = False
        else:
            print(_("entry in this team, cannot delete"))
        return

    teamselect = Menu(_("team editor {}").format(team.name))
    teamselect.textchoice = _('Your choice is ?:')
    teamselect.texterror = _('please only enter numbers between 1 and {}')
    teamselect.append(_("change team name"), editor_team)
    teamselect.append(_("team info"), info_team_sel)
    teamselect.append(_("delete team"), delete_team)
    teamselect.finish(text=_("back"))
    teamselect.run()


def edit_competition(competition):
    """
    change of data of table competition

    :type competition: competition
    :param competition: data
    """
    competition.name = inputpro(competition.name, _('name of competition'))
    competition.rule_right_winner = inputint(
        competition.rule_right_winner, _('points for right winner'))
    competition.rule_right_goaldif = inputint(
        competition.rule_right_goaldif, _('points for right goaldif'))
    competition.rule_right_result = inputint(
        competition.rule_right_result, _('points for right result'))
    competition.rule_cup_winner = inputint(
        competition.rule_cup_winner, _('point for right cup winner'))
    print(_('cup winner selection'))
    competition.cup_winner_id = int(SelectionMenu(
        session.query(model.Team).all(), finishtext=_('None')))
    return competition


def new_competition():
    """new competition

    :return:
    """
    session.add(edit_competition(model.Competition()))


def all_games_competition(competition, export):
    """
    print all games of competition

    :type competition: competition
    :param competition: data
    :type export: True/False
    :param export: write data in a file
    """
    if not competition:
        competition_id = int(SelectionMenu(session.query(
            model.Competition).all()))
        if competition_id == 0:
            return
        competition = session.query(model.Competition).filter_by(
            id=competition_id).first()

    print(_("competition: {}").format(competition.name))
    gamelist = dict(competition=competition.name, Name='', Email='', Winnerbet='', games=[])
    for game in competition.games:
        try:
            team_home_name = game.team_home.name
        except AttributeError:
            team_home_name = "no team home selected"
        try:
            team_away_name = game.team_away.name
        except AttributeError:
            team_away_name = "no team away selected"

        print('{0} : {1}'.format(team_home_name, team_away_name))
        gamelist['games'].append(dict(game_a=team_home_name,
                                      game_b=team_away_name,
                                      date=game.start_date.strftime('%Y-%m-%dT%H:%M'),
                                      tip_a='None',
                                      tip_b='None'))
    if export:
        with open("games_json.txt", "w", encoding='utf8') as f:
            f.write(json.dumps(gamelist, indent=4, sort_keys=True,
                               ensure_ascii=False))


def info_competition(competition):
    """info competition

    :param competition:
    :return:
    """
    print(_("competition: {0}, Points {1},{2},{3},{4}").
          format(competition.name,
          competition.rule_right_winner, competition.rule_right_goaldif,
          competition.rule_right_result, competition.rule_cup_winner,))
    try:
        print(_("cupwinner: {}").format(competition.teams.name))
    except AttributeError:
        print(_("no cupwinner selected"))


def select_competition():
    """select competition

    :return:
    """
    competitionid = int(SelectionMenu(session.query(
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
    info_competition_sel = functools.partial(info_competition, competition)

    def delete_competition():
        """delete competition

        :return:
        """
        if competition.cup_winner_bets == [] and competition.games == []:
            print(_("competition {} is deleted").format(competition.name))
            session.delete(competition)
            compselect.menushow = False
        else:
            print(_("entry in this competition, cannot delete"))
        return

    compselect = Menu(_("competition edit menu {}").format(competition.name))
    compselect.textchoice = _('Your choice is ?:')
    compselect.texterror = _('please only enter numbers between 1 and {}')
    compselect.append(_("competition name change"), editor_competition)
    compselect.append(_("competition info"), info_competition_sel)
    compselect.append(_("delete this competition"), delete_competition)
    compselect.append(_("add game"), new_game_competition)
    compselect.append(_("game selection"), select_game_competition)
    compselect.append(_("show all games"), print_all_games_competition)
    compselect.append(_("export all games for bets"), export_all_games_competition)
    compselect.finish(text=_("back"))
    compselect.run()


def edit_cup_winner_bet(cup_winner_bet):
    """
    change of data of table cup_winner_bet

    :type cup_winner_bet: cup_winner_bet
    :param cup_winner_bet: data
    """
    print(_('team selection'))
    cup_winner_bet.team_id = int(SelectionMenu(
        session.query(model.Team).all()))
    return cup_winner_bet


def new_cup_winner_bet(user_id, competition_id=None):
    """add a new cup winner bet

    :param user_id: data:
    :param competition_id: data
    """
    if not competition_id:
        competition_id = int(SelectionMenu(session.query(
            model.Competition).all()))
    if competition_id == 0:
        return
    session.add(edit_cup_winner_bet(model.CupWinnerBet(
        user_id=user_id, competition_id=competition_id)))


def select_cup_winner_bet(user_id, competition_id=None):
    """select cup winner bet

    :param user_id:
    :param competition_id:
    :return:
    """
    print(user_id)
    if not competition_id:
        competition_id = int(SelectionMenu(session.query(
            model.Competition).all()))
    if competition_id == 0:
        return
    memberid = int(SelectionMenu(session.query(
        model.CupWinnerBet).filter_by(
            user_id=user_id).filter_by(competition_id=competition_id).all()))
    if memberid == 0:
        return
    cup_winner_bet = session.query(model.CupWinnerBet).filter_by(
        id=memberid).first()
    editor_cup_winner_bet = functools.partial(edit_cup_winner_bet,
                                              cup_winner_bet)

    def delete_cup_winner_bet():
        session.delete(cup_winner_bet)
        cup_winner_betselect.menushow = False
        return

    cup_winner_betselect = Menu(_("cup winner bet editor {}").format(
        cup_winner_bet.teams.name))
    cup_winner_betselect.textchoice = _('Your choice is ?:')
    cup_winner_betselect.texterror = _(
        'please only enter numbers between 1 and {}')
    cup_winner_betselect.append(_("change cup winner bet"),
                                editor_cup_winner_bet)
    cup_winner_betselect.append(_("delete this bet"), delete_cup_winner_bet)
    cup_winner_betselect.finish(text=_("back"))
    cup_winner_betselect.run()


def edit_game(game):
    """
    change of data of table game

    :param game: data
    """
    print(_('team home selection'))
    game.team_home_id = int(SelectionMenu(
        session.query(model.Team).all()))
    print(_('team away selection'))
    game.team_away_id = int(SelectionMenu(
        session.query(model.Team).all()))
    game.result_home = inputpro(game.result_home, _('result home'))
    game.result_away = inputpro(game.result_away, _('result away'))
    return game


def edit_game_result(competition_id=None, game_id=None):
    """
    change of data of table game

    :param game: data
    """
    if not competition_id and not game_id:
        competition_id = int(SelectionMenu(session.query(
            model.Competition).all()))
    if competition_id == 0:
        return
    if not game_id:
        game_id = int(SelectionMenu(session.query(model.Game).filter_by(
            competition_id=competition_id).all()))
    if game_id == 0:
        return
    game = session.query(model.Game).filter_by(id=game_id).first()
    try:
        print(_("team home: {}").format(game.team_home.name))
    except AttributeError:
        print(_("no team home selected"))
    try:
        print(_("team away: {}").format(game.team_away.name))
    except AttributeError:
        print(_("no team away selected"))
    game.result_home = inputpro(game.result_home, _('result home'))
    game.result_away = inputpro(game.result_away, _('result away'))
    return game


def new_game(competition_id):
    """add new game

    :param competition_id:
    :return:
    """
    session.add(edit_game(model.Game(competition_id=competition_id)))


def select_game(competition_id):
    """select a game

    :param competition_id:
    :return:
    """
    memberid = int(SelectionMenu(session.query(model.Game).filter_by(
        competition_id=competition_id).all()))
    if memberid == 0:
        return
    game = session.query(model.Game).filter_by(id=memberid).first()
    editor_game = functools.partial(edit_game, game)
    edit_game_result_g = functools.partial(edit_game_result, game_id=game.id)

    def info_game():
        print(_("name of the competition: {}").format(game.competition.name))
        try:
            print(_("team home: {}").format(game.team_home.name))
        except AttributeError:
            print(_("no team home selected"))
        try:
            print(_("team away: {}").format(game.team_away.name))
        except AttributeError:
            print(_("no team away selected"))

    def delete_game():
        """delete a game

        :return:
        """
        session.delete(game)
        gameselect.menushow = False
        return

    def edit_game_result_reset():
        """edit game result reset

        :return:
        """
        game.result_home = None
        game.result_away = None
        return

    gameselect = Menu(_("game editor"))
    gameselect.textchoice = _('Your choice is ?:')
    gameselect.texterror = _('please only enter numbers between 1 and {}')
    gameselect.append(_("change game"), editor_game)
    gameselect.append(_("game result"), edit_game_result_g)
    gameselect.append(_("reset game result"), edit_game_result_reset)
    gameselect.append(_("team info"), info_game)
    gameselect.append(_("delete this game"), delete_game)
    gameselect.finish(text=_("back"))
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
    :param user_id: data
    :param competition_id: data
    """
    if not user_id:
        user_id = int(SelectionMenu(session.query(
            model.User).all()))
    if user_id == 0:
        return
    if not competition_id:
        competition_id = int(SelectionMenu(session.query(
            model.Competition).all()))
    if competition_id == 0:
        return
    for games in session.query(model.Game).filter_by(
            competition_id=competition_id).all():
        print(games.name)
        game_bets = session.query(model.GameBet).filter_by(
            user_id=user_id).filter_by(game_id=games.id).all()
        if game_bets:
            print('you have bet')
            for game_bet in game_bets:
                print(game_bet.name)
                edit_game_bet(game_bet)
        else:
            print('not bet')
            session.add(edit_game_bet(model.GameBet(user_id=user_id,
                                                    game_id=games.id)))


def select_game_bet(user_id=None, game_id=None):
    """select game bet

    :param user_id:
    :param game_id:
    :return:
    """
    if not user_id:
        user_id = int(SelectionMenu(session.query(
            model.User).all()))
    if user_id == 0:
        return
    if not game_id:
        game_id = int(SelectionMenu(session.query(
            model.Game).all()))
    if game_id == 0:
        return
    memberid = int(SelectionMenu(session.query(model.GameBet).filter_by(
        user_id=user_id).filter_by(game_id=game_id).all()))
    if memberid == 0:
        return
    game_bet = session.query(model.GameBet).filter_by(id=memberid).first()
    editor_game_bet = functools.partial(edit_game_bet, game_bet)

    def info_game_bet():
        """info game bet

        :return:
        """
        print(_("info of the game bet: {}").format(game_bet.name))

    def delete_game_bet():
        """delete game bet

        :return:
        """
        session.delete(game_bet)
        game_betselect.menushow = False
        return

    game_betselect = Menu(_("game bet editor {}").format(game_bet.name))
    game_betselect.textchoice = _('Your choice is ?:')
    game_betselect.texterror = _('please only enter numbers between 1 and {}')
    game_betselect.append(_("change game bet"), editor_game_bet)
    game_betselect.append(_("gamebet info"), info_game_bet)
    game_betselect.append(_("delete this bet"), delete_game_bet)
    game_betselect.finish(text=_("back"))
    game_betselect.run()


def main():
    """
    main of pycupbetting
    show the mainmenu
    """
    all_betting_export = functools.partial(all_betting, export=True)
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

    importsub = Menu(_("import/export menu"))
    importsub.append(_("all betting export (csv)"), all_betting_export)
    export_all_games_competition = functools.partial(all_games_competition,
                                                     None, True)
    importsub.append(_("export all games for bets"), export_all_games_competition)
    importsub.append(_("add competition from json"), add_json)
    importsub.append(_("add user bets from json"), importJsonUserBet)

    menu.append(_("show all betting"), all_betting)
    menu.append(_("edit game result"), edit_game_result)
    menu.append_submenu(teamsub)
    menu.append_submenu(usersub)
    menu.append_submenu(competitionsub)
    menu.append_submenu(importsub)

    # create 'Exit'-entries automatically - nice to have this :-)
    # saves a lot of typing... :-)))
    menu.finish(text=_("exit"))

    # shake it!
    menu.run()


if __name__ == "__main__":
    languagemenu = Menu("language")
    languagemenu.append("Deutsch", translation_de)
    languagemenu.append("Esperanto", translation_eo)
    languagemenu.finish(text="english")
    languagemenu.run(once=True)
    main()
