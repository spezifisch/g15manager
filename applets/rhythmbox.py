# coding: UTF-8

import subprocess

import dbus
import gobject

name = "Rhythmbox"
description = "Shows the Rhythmbox's\ncurrent track"

def start():
  
    process = subprocess.Popen(["g15composer", "/tmp/g15manager-rhythmbox"])

    cn = ["A", "A", "A", "A", "A", "E", "E", "E", "E", "I", "I", "I", "I", "D",
        "N", "O", "O", "O", "O", "x", "O", "U", "U", "U", "Y", "a", "a", "a", "a",
        "a", "c", "e", "e", "e", "e", "i", "i", "i", "i", "n", "o", "o", "o", "o",
        "o", "u", "u", "u", "AE", "ae", "a", "o", "u", "ss", "A", "O", "U","!"]


    cu = ["À", "Á", "Â", "Ã", "Å", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï", "Ð",
        "Ñ", "Ò", "Ó", "Ô", "Õ", "×", "Ø", "Ù", "Ú", "Û", "Ý", "à", "á", "â", "ã",
        "å", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï", "ñ", "ò", "ó", "ô", "õ",
        "ø", "ù", "ú", "û", "Æ", "æ", "ä", "ö", "ü", "ß", "Ä", "Ö", "Ü","¡"]

    gobject.timeout_add(1000, applet, cn, cu)

    return process

def applet(cn, cu):
    if not loop:
        return False

    bus = dbus.SessionBus()
    playerbus = bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Player')
    shell = bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Shell')

    status = playerbus.getPlaying()


    if not status:
        if playerbus.getPlayingUri():
            text = "TO 0 18 2 1 \"Paused\"\n"
        else:
            text = "TO 0 18 2 1 \"Stopped\"\n"

    else:
        try:
            uri = playerbus.getPlayingUri()
            shell.getSongProperties(uri)

            Title = shell.getSongProperties(uri)["title"]
            Artist = shell.getSongProperties(uri)["artist"]
            Album = shell.getSongProperties(uri)["album"]
            Year = shell.getSongProperties(uri)["year"]

            duration = shell.getSongProperties(uri)["duration"]
            position = playerbus.getElapsed()

        except:
            Title = ""
            Artist = ""
            Album = ""
            duration = 0
            position = 0
            Year = 0


        totm = duration / 60
        tots = duration % 60
        posm = position / 60
        poss = position % 60


        for entry in cu:
            Title = Title.replace(entry, cn[cu.index(entry)])
            Artist = Artist.replace(entry, cn[cu.index(entry)])
            Album = Album.replace(entry, cn[cu.index(entry)])


        maxlen = max([len(Title), len(Artist), len(Album)])

        if maxlen <= 20:
            text_size = 2
        elif 20 < maxlen <= 30:
            text_size = 1
        else:
            text_size = 0

            if len(Title) > 40:
                Title = Title[(poss % (len(Title) - 38)):]
            if len(Artist) > 40:
                Artist = Artist[(poss % (len(Artist) - 38)):]
            if len(Album) > 40:
                Album = Album[(poss % (len(Album) - 38)):]

        if poss < 10:
            poss = str(poss)
            poss = poss.replace(poss, "0" + poss)
        if tots < 10:
            tots = str(tots)
            tots = tots.replace(tots, "0" + tots)


        text = "MC 1\n" + \
            "PC 0\n" + \
            "TO 0 2 %i 1 \"%s\"\n" % (text_size, Title) + \
            "DL 0 11 158 11 1\n" + \
            "TO 0 14 %i 1 \"%s\"\n" % (text_size, Artist) + \
            "TO 0 22 %i 1 \"%s\"\n" % (text_size, Album)  + \
            "DB 0 32 159 32 1 %i %i \n" % (position, duration) + \
            "TO 0 36 1 0\"%i:%s\"\n" % (posm, poss) + \
            "TO 0 36 1 1 \"%s\"\n" % Year + \
            "TO 0 36 1 2 \"%i:%s\"\n" % (totm, tots) + \
            "MC 0\n";


    with open("/tmp/g15manager-rhythmbox", "w") as pipe:
        pipe.write(text)

    return loop