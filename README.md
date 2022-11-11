pycupbetting
============

[![Join the chat at https://gitter.im/MarkusHackspacher/pycupbetting](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/MarkusHackspacher/pycupbetting?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

The idea is the preliminary round and the winner to tap. 
I would like to realize with the python programming language. 

Basic functions
---------------

The basic functions would print all the games on one side and then make them
the tipsters to fill at your disposal, of course, the tip and result input.
In addition, the income statement for the right wins there is a point, the
right goal differnce two points and the correct score three points.
And the expression of the result, the whole thing would realized in the first
step without a GUI, the entries should be made in the command line.
The data are stored in a database, preferably SQLite.

installation and start
----------------------

The [pycupbetting](https://github.com/MarkusHackspacher/pycupbetting) requires [Python 3.x](http://www.python.org/download/)
and [sqlalchemy](http://www.sqlalchemy.org/).
Download und install Python and

```
easy_install SQLAlchemy
```
or
```
pip install SQLAlchemy
```
Windows:
```
py -m pip install SQLAlchemy
```
Then you copied the source code of the program on your computer,
either [download](https://github.com/MarkusHackspacher/pycupbetting/archive/refs/heads/master.zip) the zip file of the project or download with the version control system:

```
# git clone https://github.com/MarkusHackspacher/pycupbetting.git
```
change the directory with:
```
cd pycupbetting
python3 pycupbetting.py
```
Windows:
```
py pycupbetting.py
```
to run the program.

translation
-----------

For the translation use to make a messages.pot file

```
pygettext3 pycupbetting.py
```

rename the file in messages_xx.po and translate it.
To converts to a binary GNU catalog (.mo file) use msgfmt. Example for german:

```
msgfmt locale/de/messages_de.po -o locale/de/LC_MESSAGES/pycupbetting.mo
```

license
-------

GNU GPL

database draw
-------------

the file DB-Entwurf.xmi is make by:

Umbrello UML-Modeller
© 2001 Paul Hensgen, © 2002–2006 Umbrello UML-Modeller-Autoren
http://uml.sf.net/
