#!/usr/bin/python
# coding: UTF-8

from distutils.core import setup

setup (
    name = 'G15 Manager',
    version = '0.1',
    author = 'Nofre Móra',
    author_email = 'nodiek@gmail.com',
    url = 'https://launchpad.net/g15manager',
    license = 'GPL',
    description= 'An easy way to manage the applets of a G15 keyboard and bind the G-Keys',

    data_files=[
    ('/usr/bin', ['g15manager']),
    ('/usr/share/g15manager' , ['g15manager.py','g15manager.ui']),
    ('/usr/share/g15manager/applets', ['applets/__init__.py','applets/amarok.py','applets/audacious.py',
            'applets/emesene.py','applets/exaile.py','applets/gmail.py','applets/top.py']),
    ('/usr/share/g15manager/icons', ['icons/g15.png', 'icons/g15stats.png', 'icons/gkeys.png','icons/gmail.png']),
    ('/usr/share/applications',['g15manager.desktop'])]

)

