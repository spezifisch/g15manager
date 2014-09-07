QT       += core gui dbus

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = G15Manager
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
    applets/gmailapplet.cpp \
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
    applets/gmailapplet.h \
    applets/hardwareapplet.h \
    applets/processesapplet.h \
    applets/rhythmboxapplet.h \
    applets/cronoapplet.h

FORMS    += mainwindow.ui

OTHER_FILES +=
