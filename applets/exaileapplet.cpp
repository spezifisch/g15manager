#include <QString>
#include <QDBusMessage>
#include <QDBusConnection>
#include <QDBusReply>

#include "exaileapplet.h"

exaileApplet::exaileApplet() : Applet() {}

exaileApplet::~exaileApplet() {}

void exaileApplet::update() {
    QDBusMessage m = QDBusMessage::createMethodCall((QString)"org.exaile.Exaile",(QString)"/org/exaile/Exaile","",(QString)"IsPlaying");
    QDBusReply<bool> isPlaying = QDBusConnection::sessionBus().call(m);

    g15r_clearScreen(canvas, 0);

    if (!isPlaying.isValid()) {
        g15r_G15FPrint (canvas, (char *) "Exaile", 0, -4, G15_TEXT_HUGE, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 1);
        g15r_G15FPrint (canvas, (char *) "Not Running", 0, 0, G15_TEXT_HUGE, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 2);
    }
    else {

        if (!isPlaying) g15r_G15FPrint (canvas, (char *) "Stopped", 0, 0, G15_TEXT_LARGE, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 2);

        else {

            m = QDBusMessage::createMethodCall((QString)"org.exaile.Exaile",(QString)"/org/exaile/Exaile","",(QString)"GetTrackAttr");
            QList<QVariant> args;
            args.append("title");
            m.setArguments(args);
            QDBusReply<QString> result = QDBusConnection::sessionBus().call(m);
            QString title = eliminarAccents(result.value());

            m = QDBusMessage::createMethodCall((QString)"org.exaile.Exaile",(QString)"/org/exaile/Exaile","",(QString)"GetTrackAttr");
            args.clear();
            args.append("artist");
            m.setArguments(args);
            result = QDBusConnection::sessionBus().call(m);
            QString artist = eliminarAccents(result.value());

            m = QDBusMessage::createMethodCall((QString)"org.exaile.Exaile",(QString)"/org/exaile/Exaile","",(QString)"GetTrackAttr");
            args.clear();
            args.append("album");
            m.setArguments(args);
            result = QDBusConnection::sessionBus().call(m);
            QString album = eliminarAccents(result.value());

            m = QDBusMessage::createMethodCall((QString)"org.exaile.Exaile",(QString)"/org/exaile/Exaile","",(QString)"GetTrackAttr");
            args.clear();
            args.append("year");
            m.setArguments(args);
            result = QDBusConnection::sessionBus().call(m);
            QString year = result.value()+"2000";


            m = QDBusMessage::createMethodCall((QString)"org.exaile.Exaile",(QString)"/org/exaile/Exaile","",(QString)"GetTrackAttr");
            args.clear();
            args.append("__length");
            m.setArguments(args);
            result = QDBusConnection::sessionBus().call(m);
            int length = QString(result.value()).toFloat();


            m = QDBusMessage::createMethodCall((QString)"org.exaile.Exaile",(QString)"/org/exaile/Exaile","",(QString)"CurrentPosition");
            result = QDBusConnection::sessionBus().call(m);
            QString strtemps = result.value();
            if (strtemps.length() == 4) strtemps.insert(0, '0');

            m = QDBusMessage::createMethodCall((QString)"org.exaile.Exaile",(QString)"/org/exaile/Exaile","",(QString)"CurrentProgress");
            result = QDBusConnection::sessionBus().call(m);
            int progress = result.value().toInt()*1.6;

            int totm = length / 60;
            int tots = length % 60;


            int maxlen = std::max(title.length(), std::max(artist.length(), album.length()));
            int text_size = G15_TEXT_SMALL;

            if (maxlen <= 20) text_size = G15_TEXT_LARGE;
            else if (maxlen > 20 && maxlen <= 30) text_size = G15_TEXT_MED;
            else {
                if (title.length() > 40) title = title.right(title.length()-(progress % (title.length()-38)));
                if (artist.length() > 40) artist = artist.right(artist.length()-(progress % (artist.length()-38)));
                if (album.length() > 40) album = album.right(album.length()-(progress % (album.length()-38)));
            }


            strtemps.append("/");

            if (totm < 10) strtemps.append("0");
            strtemps.append(QString::number(totm));
            strtemps.append(":");
            if (tots < 10) strtemps.append("0");
            strtemps.append(QString::number(tots));

            g15r_G15FPrint (canvas, qstringToChar(title), 0, 0, text_size, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 0);
            g15r_G15FPrint (canvas, qstringToChar(artist), 0, 0, text_size, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 1);
            g15r_G15FPrint (canvas, qstringToChar(album), 0, 0, text_size, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 2);

            g15r_pixelBox(canvas, 0, 28, progress, 32, G15_COLOR_BLACK, 1, G15_PIXEL_FILL);
            g15r_pixelBox(canvas, progress, 28, 159, 32, G15_COLOR_BLACK, 1, G15_PIXEL_NOFILL);

            g15r_G15FPrint (canvas, qstringToChar(year), 4, 0, G15_TEXT_MED, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 5);
            g15r_G15FPrint (canvas, qstringToChar(strtemps), 0, 0, G15_TEXT_MED, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 5);
        }
    }

    g15_send(fd, (char *) canvas->buffer, G15_BUFFER_LEN);
}
