QT       += core gui dbus

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = g15manager
TEMPLATE = app

LIBS += /usr/lib/libg15.so \
    /usr/lib/libg15daemon_client.so \
    /usr/lib/libg15render.so


SOURCES += main.cpp\
    mainwindow.cpp \
    appletsManager.cpp \
    applets/amarokapplet.cpp \
    applets/applet.cpp \
    applets/audaciousapplet.cpp \
    applets/clementineapplet.cpp \
    applets/exaileapplet.cpp \
    applets/hardwareapplet.cpp \
    applets/processesapplet.cpp \
    applets/chronoapplet.cpp

HEADERS  += mainwindow.h \
    appletsManager.h \
    applets/amarokapplet.h \
    applets/applet.h \
    applets/audaciousapplet.h \
    applets/clementineapplet.h \
    applets/exaileapplet.h \
    applets/hardwareapplet.h \
    applets/processesapplet.h \
    applets/chronoapplet.h

FORMS    += mainwindow.ui

binaries.path = /usr/bin
binaries.files = g15manager

icons.path = /usr/share/g15manager/icons
icons.files = icons/*

autostart.path = /etc/xdg/autostart
autostart.files = shortcuts/g15manager_autostart.desktop

shortcuts.path = /usr/share/applications
shortcuts.files = shortcuts/g15manager.desktop

manpage.path = /usr/share/man/man1
manpage.files = man/g15manager.1.gz

INSTALLS = binaries icons autostart shortcuts manpage
