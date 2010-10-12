#!/usr/bin/python
# coding: UTF-8

from distutils.core import setup

setup (
    name = 'G15 Manager',
    version = '0.3.2',
    author = 'Nofre Móra',
    author_email = 'nodiek@gmail.com',
    url = 'https://launchpad.net/g15manager',
    license = 'GPL',
    description= 'A control center for the Logitech G15 keyboard',

    data_files=[

    ('/usr/bin', ['g15manager']),

    ('/usr/share/g15manager' , ['g15manager.py','g15manager.ui','keys.py']),

    ('/usr/share/g15manager/applets', ['applets/__init__.py','applets/amarok.py','applets/audacious.py',
            'applets/emesene.py','applets/exaile.py','applets/gmail.py','applets/top.py','applets/rhythmbox.py','applets/hardmon.py']),

    ('/usr/share/g15manager/icons', ['icons/g15.png','icons/gkeys.png','icons/gmail.png','icons/config.png']),

    ('/usr/share/applications', ['g15manager.desktop']),

	('/usr/share/locale/ca/LC_MESSAGES', ['po/ca/g15manager.mo']),
	('/usr/share/locale/es/LC_MESSAGES', ['po/es/g15manager.mo']),

]
)

