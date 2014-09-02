#include <QString>
#include <QDBusMessage>
#include <QDBusConnection>
#include <QDBusReply>


#include "rhythmboxapplet.h"

rhythmboxApplet::rhythmboxApplet() : Applet() {}


void rhythmboxApplet::update() {
    QDBusMessage m = QDBusMessage::createMethodCall((QString)"org.mpris.amarok",(QString)"/Player","",(QString)"GetMetadata");
    QDBusReply<QVariantMap> result = QDBusConnection::sessionBus().call(m);

    QString text;

    if (!result.isValid()) {
        g15r_G15FPrint (canvas, (char *) "Rhythmbox", 0, 0, G15_TEXT_HUGE, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 1);
        g15r_G15FPrint (canvas, (char *) "Not Found", 0, 0, G15_TEXT_HUGE, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 2);
    }
    else {

        QVariantMap map = result.value();

        QString title = eliminarAccents(map.find("title").value().toString());
        QString artist = eliminarAccents(map.find("artist").value().toString());
        QString album = eliminarAccents(map.find("album").value().toString());
        QString year = map.find("year").value().toString();
        int length = map.find("mtime").value().toInt()/1000;


        m = QDBusMessage::createMethodCall((QString)"org.mpris.amarok",(QString)"/Player","",(QString)"PositionGet");
        QDBusReply<int> rpos = QDBusConnection::sessionBus().call(m);
        int position = rpos.value()/1000;

        int totm = length / 60;
        int tots = length % 60;
        int posm = position / 60;
        int poss = position % 60;


        int maxlen = std::max(title.length(), std::max(artist.length(), album.length()));
        QString text_size = "0";

        if (maxlen <= 20) text_size = "2";
        else if (maxlen > 20 && maxlen <= 30) text_size = "1";
        else {
            if (title.length() > 40) title = title.right(title.length()-(poss % (title.length()-38)));
            if (artist.length() > 40) artist = artist.right(artist.length()-(poss % (artist.length()-38)));
            if (album.length() > 40) album = album.right(album.length()-(poss % (album.length()-38)));
        }

        QString strtotal;
        if (totm < 10) strtotal.append("0");
        strtotal.append(QString::number(totm));
        strtotal.append(":");
        if (tots < 10) strtotal.append("0");
        strtotal.append(QString::number(tots));

        QString strpos;
        if (posm < 10) strpos.append("0");
        strpos.append(QString::number(posm));
        strpos.append(":");
        if (poss < 10) strpos.append("0");
        strpos.append(QString::number(poss));

        text = "MC 1\n";
        text.append("PC 0\n");
        text.append(QString("TO 0 2 %1 1 \"%2\"\n").arg(text_size, title));
        text.append("DL 0 11 158 11 1\n");
        text.append(QString("TO 0 14 %1 1 \"%2\"\n").arg(text_size, artist));
        text.append(QString("TO 0 22 %1 1 \"%2\"\n").arg(text_size, album));
        text.append(QString("DB 0 32 159 32 1 %1 %2\n").arg(position).arg(length));
        text.append(QString("TO 0 36 1 0 \"%1\"\n").arg(strpos));
        text.append(QString("TO 0 36 1 1 \"%1\"\n").arg(year));
        text.append(QString("TO 0 36 1 2 \"%1\"\n").arg(strtotal));
        text.append("MC 0\n");
    }

    g15_send(fd, (char *) canvas->buffer, G15_BUFFER_LEN);
}
