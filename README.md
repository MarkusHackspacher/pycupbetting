pycupbetting
============

The idea is the preliminary round and the winner to tap. 
I would like to realize with the python programming language. 

Die Idee ist die Vorrunde und den Sieger zu Tippen.
Das möchte ich mit der Programmiersprache Python realisieren. 

Basic functions
--------------

The basic functions would print all the games on one side and then make them
the tipsters to fill at your disposal, of course, the tip and result input.
In addition, the income statement for the right wins there is a point, the
right goal differnce two points and the correct score three points.
And the expression of the result, the whole thing would realized in the first
step without a GUI, the entries should be made in the command line.
The data are stored in a database, preferably SQLite.

Grundfunktionen
---------------
Die Grundfunktionen wären alle Spiele auf eine Seite auszudrucken und dann
diese den Tipper zum Ausfüllen zu Verfügung stellen, natürlich  auch die
Tipp- und Ergebnisseingabe. Dazu kommt die Ergebnissrechnung, für den richtigen
Siegen gibt es einen Punkt, für den richtigen Torabstand zwei Punkte und für
das exakte richtige Ergebniss drei Punkte. Und den Ausdruck des Ergebniss, das
Ganze möchte im ersten Schritt ohne GUI realisiert, die Eingaben sollen in der
Kommandozeile gemacht werden. Die Daten werden in einer Datenbank,
vorzugsweise SQlite, gespeichert.

translation
-----------
For the translation use fro make a messages.pot file
```pygettext3 pycupbetting.py```
rename the file in messages.po and translate it.
To make a computer use file:
```msgfmt messages.po -o locale/de/LC_MESSAGES/pycupbetting.mo```

license
-------
GNU GPL

database draw
-------------
the file DB-Entwurf.xmi is make by:

Umbrello UML-Modeller
© 2001 Paul Hensgen, © 2002–2006 Umbrello UML-Modeller-Autoren
http://uml.sf.net/
