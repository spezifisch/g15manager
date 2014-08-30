#-------------------------------------------------
#
# Project created by QtCreator 2014-05-07T12:21:47
#
#-------------------------------------------------

QT       += core gui dbus

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = G15Manager
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    appletsManager.cpp \
    clementineapplet.cpp \
    amarokapplet.cpp \
    applet.cpp \
    audaciousapplet.cpp \
    exaileapplet.cpp \
    gmailapplet.cpp \
    processesapplet.cpp \
    rhythmboxapplet.cpp \
    hardwareapplet.cpp

HEADERS  += mainwindow.h \
    appletsManager.h \
    clementineapplet.h \
    amarokapplet.h \
    applet.h \
    audaciousapplet.h \
    exaileapplet.h \
    gmailapplet.h \
    hardwareapplet.h \
    processesapplet.h \
    rhythmboxapplet.h

FORMS    += mainwindow.ui
