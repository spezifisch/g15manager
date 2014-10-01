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
    applets/rhythmboxapplet.cpp \
    applets/cronoapplet.cpp

HEADERS  += mainwindow.h \
    appletsManager.h \
    applets/amarokapplet.h \
    applets/applet.h \
    applets/audaciousapplet.h \
    applets/clementineapplet.h \
    applets/exaileapplet.h \
    applets/hardwareapplet.h \
    applets/processesapplet.h \
    applets/rhythmboxapplet.h \
    applets/cronoapplet.h

FORMS    += mainwindow.ui

binaries.path = /usr/bin
binaries.files = g15manager

icons.path = /usr/share/g15manager/icons
icons.files = icons/*

autostart.path = /etc/xdg/autostart
autostart.files = shortcuts/g15manager_autostart.desktop

shortcuts.path = /usr/share/applications
shortcuts.files = shortcuts/g15manager.desktop

INSTALLS = binaries icons autostart shortcuts
