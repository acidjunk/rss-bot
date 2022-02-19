RSS to Twitter bot
==================

Very WIP; sorry no fancy intro yet. Feel free to open a PR.

Running tests:
```
$ py.test # or execute py.test from any sub folder in unit_tests/
$ pt.test -n auto
```

Changelog
---------
*v0.1*
- added working Config stuff that can be set via ENV vars
- added license
- added a simple feed retriever that knows if the feed has changed
- added a simple HTML stripper
- implemented tweet via tweet-hs


License
-------
Copyright (C) 2019 René Dohmen <acidjunk@gmail.com>

Licensed under the GNU GENERAL PUBLIC LICENSE Version 3
A copy of the LICENSE is included in the project.