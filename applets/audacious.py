# coding: UTF-8

import subprocess

import dbus
import gobject

def start():
  
    process = subprocess.Popen(["g15composer", "/tmp/g15manager-audacious"])

    cn = ["A", "A", "A", "A", "A", "E", "E", "E", "E", "I", "I", "I", "I", "D",
        "N", "O", "O", "O", "O", "x", "O", "U", "U", "U", "Y", "a", "a", "a", "a",
        "a", "c", "e", "e", "e", "e", "i", "i", "i", "i", "n", "o", "o", "o", "o",
        "o", "u", "u", "u", "AE", "ae", "a", "o", "u", "ss", "A", "O", "U"]


    cu = ["À", "Á", "Â", "Ã", "Å", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï", "Ð",
        "Ñ", "Ò", "Ó", "Ô", "Õ", "×", "Ø", "Ù", "Ú", "Û", "Ý", "à", "á", "â", "ã",
        "å", "ç", "è", "é", "ê", "ë", "ì", "í", "î", "ï", "ñ", "ò", "ó", "ô", "õ",
        "ø", "ù", "ú", "û", "Æ", "æ", "ä", "ö", "ü", "ß", "Ä", "Ö", "Ü"]

    gobject.timeout_add(1000, applet, cn, cu)

    return process

def applet(cn, cu):
    if not loop:
        return False

    try:
        bus = dbus.SessionBus()
        playerbus = bus.get_object('org.mpris.audacious', '/Player')

        status = playerbus.GetStatus()[0]

        if status == 2:
            text = "TO 0 18 2 1 \"Stopped\"\n"

        elif status == 1:
            text = "TO 0 18 2 1 \"Paused\"\n"

        elif status == 0:
            try:
                info = playerbus.GetMetadata()
                Title = str(info[u'title'])
                Artist = str(info[u'artist'])
                Album = str(info[u'album'])
                try:
                    Year = str(info[u'year'])
                except:
                    Year = " "

                time = info[u'mtime'] / 1000

            except:
                Title = ""
                Artist = ""
                Album = ""
                time = 0
                Year = 0


            position = playerbus.PositionGet() / 1000
            totm = time / 60
            tots = str(time % 60)
            posm = position / 60
            poss = str(position % 60)

            if int(poss) < 10:
                poss = poss.replace(poss, "0" + poss)
            if int(tots) < 10:
                tots = tots.replace(tots, "0" + tots)


            for entry in cu:
                Title = Title.replace(entry, cn[cu.index(entry)])
                Artist = Artist.replace(entry, cn[cu.index(entry)])
                Album = Album.replace(entry, cn[cu.index(entry)])

            if len(Title) <= 20:
                text_size = 2
            elif 20 < len(Title) <= 30:
                text_size = 1
            elif len(Title) > 30:
                text_size = 0


            text = "MC 1\n" + \
                "PC 0\n" + \
                "TO 0 2 %i 1 \"%s\"\n" % (text_size, Title) + \
                "DL 0 11 158 11 1\n" + \
                "TO 0 14 %i 1 \"%s\"\n" % (text_size, Artist) + \
                "TO 0 22 %i 1 \"%s\"\n" % (text_size, Album)  + \
                "DB 0 32 159 32 1 %i %i \n" % (position, time) + \
                "TO 0 36 1 0\"%i:%s\"\n" % (posm, poss) + \
                "TO 0 36 1 1 \"%s\"\n" % Year + \
                "TO 0 36 1 2 \"%i:%s\"\n" % (totm, tots) + \
                "MC 0\n";


    except:
        text =  "TO 0 18 1 1 \"Audacious isn't running\"\n"

    with open("/tmp/g15manager-audacious", "w") as pipe:
        pipe.write(text)

    return loop