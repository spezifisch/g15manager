#include <QString>
#include <QDBusMessage>
#include <QDBusConnection>
#include <QDBusReply>


#include "audaciousapplet.h"

audaciousApplet::audaciousApplet() : Applet() {}


void audaciousApplet::update() {

    QDBusMessage m = QDBusMessage::createMethodCall((QString)"org.mpris.audacious",(QString)"/Player","",(QString)"GetMetadata");
    QDBusReply<QVariantMap> result = QDBusConnection::sessionBus().call(m);

    g15r_clearScreen(canvas, 0);

    if (!result.isValid()) {
        g15r_G15FPrint (canvas, (char *) "Audacious", 0, 0, G15_TEXT_HUGE, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 1);
        g15r_G15FPrint (canvas, (char *) "Not Found", 0, 0, G15_TEXT_HUGE, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 2);
    }
    else {

        QVariantMap map = result.value();

        QString title = eliminarAccents(map.find("title").value().toString());
        QString artist = eliminarAccents(map.find("artist").value().toString());
        QString album = eliminarAccents(map.find("album").value().toString());
        QString year = map.find("year").value().toString();
        int length = map.find("mtime").value().toInt()/1000;


        m = QDBusMessage::createMethodCall((QString)"org.mpris.audacious",(QString)"/Player","",(QString)"PositionGet");
        QDBusReply<int> rpos = QDBusConnection::sessionBus().call(m);
        int position = rpos.value()/1000;

        int totm = length / 60;
        int tots = length % 60;
        int posm = position / 60;
        int poss = position % 60;


        int maxlen = std::max(title.length(), std::max(artist.length(), album.length()));
        int text_size = G15_TEXT_SMALL;

        if (maxlen <= 20) text_size = G15_TEXT_LARGE;
        else if (maxlen > 20 && maxlen <= 30) text_size = G15_TEXT_MED;
        else {
            if (title.length() > 40) title = title.right(title.length()-(poss % (title.length()-38)));
            if (artist.length() > 40) artist = artist.right(artist.length()-(poss % (artist.length()-38)));
            if (album.length() > 40) album = album.right(album.length()-(poss % (album.length()-38)));
        }

        QString strtemps;
        if (posm < 10) strtemps.append("0");
        strtemps.append(QString::number(posm));
        strtemps.append(":");
        if (poss < 10) strtemps.append("0");
        strtemps.append(QString::number(poss));

        strtemps.append("/");

        if (totm < 10) strtemps.append("0");
        strtemps.append(QString::number(totm));
        strtemps.append(":");
        if (tots < 10) strtemps.append("0");
        strtemps.append(QString::number(tots));


        int progress = float(position)/float(length)*160;

        g15r_G15FPrint (canvas, qstringToChar(title), 0, 0, text_size, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 0);
        g15r_G15FPrint (canvas, qstringToChar(artist), 0, 0, text_size, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 1);
        g15r_G15FPrint (canvas, qstringToChar(album), 0, 0, text_size, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 2);

        g15r_pixelBox(canvas, 0, 28, progress, 32, G15_COLOR_BLACK, 1, G15_PIXEL_FILL);
        g15r_pixelBox(canvas, progress, 28, 159, 32, G15_COLOR_BLACK, 1, G15_PIXEL_NOFILL);

        g15r_G15FPrint (canvas, qstringToChar(year), 0, 0, G15_TEXT_MED, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 5);
        g15r_G15FPrint (canvas, qstringToChar(strtemps), 0, 0, G15_TEXT_MED, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 5);
        //g15r_G15FPrint (canvas, qstringToChar(strtotal), 0, 0, G15_TEXT_MED, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 5);
    }

    g15_send(fd, (char *) canvas->buffer, G15_BUFFER_LEN);
}
