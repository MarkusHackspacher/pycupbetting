#!/usr/bin/env python

#
#  Copyright (C) 2012  Christian Hausknecht
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    ~~~~~~~~~~~~~
    classymenu.py
    ~~~~~~~~~~~~~

    The most advanced module to create and handle menus with basic Python
    kwnoledges.

    This time we use a class to represent and handle our menu tasks.

    It might be understandable even for newbies, but you should have been
    familiar to classes in Python.

    Of course the core ideas do not differ from the other, structure and
    function based approaches within this folder. As you can see a class is
    often the more comfortable way to handle deeply nested data structures.

    Our latest approach in `metamenu.py` handles tuples in a dictionary
    in a dictionary... that ist not very comfortable to deal with. You can
    get confused by indexes and perhaps keys. It feels less clumsy to deal
    with attributes of a class.

    .. moduleauthor:: Christian Hausknecht <christian.hausknecht@gmx.de>
"""

import sys
from itertools import chain

from modules import model
from sqlalchemy import orm
from sqlalchemy import create_engine

# Create an engine and create all the tables we need
engine = create_engine('sqlite:///dbcupbetting.sqlite', echo=False)
model.Base.metadata.bind = engine
model.Base.metadata.create_all(engine)

# Set up the session
sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=True,
    expire_on_commit=True)
session = orm.scoped_session(sm)


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
    userid = []
    for all_user in session.query(model.User).all():
        print ("User Nummer: {} Name: {}, Vollername: {}, ".
            format(all_user.id, all_user.name, all_user.fullname))
        userid.append(all_user.id)
    select_id = input('User Nummer:')
    if not (int(select_id) in userid):
        return
    user = session.query(model.User).filter_by(id=select_id).first()

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
    teamid = []
    for all_teams in session.query(model.Team).all():
        print ("Team Nummer: {} Name: {}".
            format(all_teams.id, all_teams.name))
        teamid.append(all_teams.id)
    select_id = input('Team Nummer:')
    if not (int(select_id) in teamid):
        return
    team = session.query(model.Team).filter_by(id=select_teamid).first()

    def editor_team():
        edit_team(team)

    def info_team():
        print ("Teamname: {}".format(team.name))

    teamselect = Menu("Teameditormenü")
    teamselect.append("Teamnamen ändern", editor_team)
    teamselect.append("Teaminfo", info_team)
    teamselect.finish()
    teamselect.run()


class Menu:
    """
    Class that represents and handles a complete menu system all in once.

    Each menu class can...

        ... print out the (current) menu
        ... handle the user input
        ... run in an event-loop, that handles the complete menu based
            workflow.

    It provides the `finish`-method, which adds automatically all needed
    'Exit'-entries to each (sub)menu, so building up a menu is not so much
    typing.

    To avoid recursion, we use the `context`-attribute of the Menu-class. The
    current menu-object is always bound to this attribute. As we can combine
    arbitrary menu objects (via the `append_submenu`-method) we must keep
    the current working menu accessible to operate only in one object, the
    'root'-object.
    """

    def __init__(self, title):
        self.title = title
        self.items = []
        self.context = self

    def __repr__(self):
        return "Menu({})".format(self.title)

    def __str__(self):
        head = ("", "-" * len(self.title), "{}".format(self.title),
                "-" * len(self.title))
        entries = ("{} {} {}".format(
                        index, "+" if isinstance(entry[1], Menu) else " ",
                        entry[0]
                    )
                    for index, entry in enumerate(self, 1)
        )
        return "\n".join(chain(head, entries))

    def __getitem__(self, key):
        """
        Nice to have method for providing the iterable "interface". So you can
        access any menu item via an index or loop over all entries using
        `for` :-)
        """
        return self.items[key]

    def append(self, text, func):
        """
        Appends a menu entry to `self.items`.

        :param text: string with entry description
        :param func: callable that will be called if chosen
        """
        self.items.append((text, func))

    def append_submenu(self, other):
        """
        Appends a submenu entry to the menu. That can be a complex branch
        of menu-objects.

        :param other: Menu object, that represents a complete submenu-branch.
        """
        self.items.append((other.title, other))

    def finish(self, text="Exit"):
        """
        Nice helper method that computes all needed 'Exit'-items for each
        submenu and the 'final' 'Exit'-item at the main-menu, which is simply
        any string.

        All other exit-items are menu objects of the corresponding parent-menu.

        The algorithm implements a breadth-first search for handling this task.

        :param text: string with the text of the 'Exit'-item.
        """
        self.items.append((text, "#exit"))
        stack = [(self, None)]
        while stack:
            menu, parent = stack.pop()
            for _, command in menu:
                if isinstance(command, Menu):
                    stack.append((command, menu))
            if menu is not self:
                menu.append("{} -> {}".format(text, parent.title), parent)

    def get_user_input(self):
        while True:
            try:
                choice = int(input("Ihre Wahl?: ")) - 1
                if 0 <= choice < len(self.context.items):
                    return choice
                else:
                    raise IndexError
            except (ValueError, IndexError):
                print("Bitte nur Zahlen aus dem Bereich 1..{} eingeben".format(
                                                    len(self.context.items)))

    def run(self):
        """
        Core method to handle a menu. This invokes a loop that handles all
        menu tasks as long as the main menu is exited by the user.
        """
        while True:
            print(self.context)
            choice = self.get_user_input()
            _, command = self.context[choice]
            if isinstance(command, Menu):
                self.context = command
            elif isinstance(command, str):
                return
            else:
                command()


def main():
    # We build up some demonstration menu as in the other menu systems.
    # Now we can use classes to create menu objects...
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
