pycupbetting
============

[![Join the chat at https://gitter.im/MarkusHackspacher/pycupbetting](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/MarkusHackspacher/pycupbetting?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

The idea is the preliminary round and the winner to tap. 
I would like to realize with the python programming language. 

Basic functions
--------------

The basic functions would print all the games on one side and then make them
the tipsters to fill at your disposal, of course, the tip and result input.
In addition, the income statement for the right wins there is a point, the
right goal differnce two points and the correct score three points.
And the expression of the result, the whole thing would realized in the first
step without a GUI, the entries should be made in the command line.
The data are stored in a database, preferably SQLite.

installation and start
----------------------
The program requires [Python 3.x](http://www.python.org/download/)
and [sqlalchemy](http://www.sqlalchemy.org/).
Install at first Python and ```easy_install SQLAlchemy``` or 
```pip install SQLAlchemy```
Start ```python3 pycupbetting.py``` to run the program.

translation
-----------
For the translation use to make a messages.pot file
```
pygettext3 pycupbetting.py
```
rename the file in messages_xx.po and translate it.
To make a computer useed file, example for german:
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
