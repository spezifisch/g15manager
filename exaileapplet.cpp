#include <QString>
#include <QDBusMessage>
#include <QDBusConnection>
#include <QDBusReply>
#include <QDebug>

#include "exaileapplet.h"

exaileApplet::exaileApplet() : Applet() {
    name = "exaile";
    //startComposer();
}


void exaileApplet::update() {
    QDBusMessage m = QDBusMessage::createMethodCall((QString)"org.exaile.Exaile",(QString)"/org/exaile/Exaile","",(QString)"IsPlaying");
    QDBusReply<bool> isPlaying = QDBusConnection::sessionBus().call(m);

    QString text;

    if (!isPlaying.isValid()) text = "MC 1\nPC 0\nTO 0 2 1 1 \"Exaile\"\nTO 0 14 1 1 \"Not Found\"\nMC 0\n";
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


        m = QDBusMessage::createMethodCall((QString)"org.mpris.clementine",(QString)"/Player","",(QString)"CurrentPosition");
        result = QDBusConnection::sessionBus().call(m);
        QString position = result.value();

        m = QDBusMessage::createMethodCall((QString)"org.mpris.clementine",(QString)"/Player","",(QString)"CurrentProgress");
        result = QDBusConnection::sessionBus().call(m);
        int progress = result.value().toInt();

        int totm = length / 60;
        int tots = length % 60;


        int maxlen = std::max(title.length(), std::max(artist.length(), album.length()));
        QString text_size = "0";

        if (maxlen <= 20) text_size = "2";
        else if (maxlen > 20 && maxlen <= 30) text_size = "1";
        else {
            if (title.length() > 40) title = title.right(title.length()-(progress % (title.length()-38)));
            if (artist.length() > 40) artist = artist.right(artist.length()-(progress % (artist.length()-38)));
            if (album.length() > 40) album = album.right(album.length()-(progress % (album.length()-38)));
        }

        QString strtotal;
        if (totm < 10) strtotal.append("0");
        strtotal.append(QString::number(totm));
        strtotal.append(":");
        if (tots < 10) strtotal.append("0");
        strtotal.append(QString::number(tots));



        text = "MC 1\n";
        text.append("PC 0\n");
        text.append(QString("TO 0 2 %1 1 \"%2\"\n").arg(text_size, title));
        text.append("DL 0 11 158 11 1\n");
        text.append(QString("TO 0 14 %1 1 \"%2\"\n").arg(text_size, artist));
        text.append(QString("TO 0 22 %1 1 \"%2\"\n").arg(text_size, album));
        text.append(QString("DB 0 32 159 32 1 %1 100\n").arg(progress));
        text.append(QString("TO 0 36 1 0 \"%1\"\n").arg(position));
        text.append(QString("TO 0 36 1 1 \"%1\"\n").arg(year));
        text.append(QString("TO 0 36 1 2 \"%1\"\n").arg(strtotal));
        text.append("MC 0\n");
    }

    //sendComposer(text);
}
