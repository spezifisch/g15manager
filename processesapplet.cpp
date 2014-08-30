#include <QProcess>
#include <QDebug>

#include "processesapplet.h"

processesApplet::processesApplet() : Applet() {
    name = "processes";
    startComposer();
}


void processesApplet::update() {

    QProcess top;
    QString program = "top";
    QStringList arguments;

    arguments.append("-b");
    arguments.append("-n");
    arguments.append("1");

    top.start(program, arguments);
    top.waitForFinished();

    QStringList linies = QString(top.readAllStandardOutput()).split("\n");
    QStringList procs;

    procs.append(linies.at(7));
    procs.append(linies.at(8));
    procs.append(linies.at(9));
    procs.append(linies.at(10));

    QStringList p1 = procs.at(0).split(QRegExp("\\s+"));
    QStringList p2 = procs.at(1).split(QRegExp("\\s+"));
    QStringList p3 = procs.at(2).split(QRegExp("\\s+"));
    QStringList p4 = procs.at(3).split(QRegExp("\\s+"));

    QString text = "MC 1\n";
    text.append("TO 0  0 2 1 \"Process Monitor\"\n");
    text.append(QString("TO 0 10 1 0 \"%1\"\n").arg(p1.at(1)));
    text.append(QString("TO 0 10 1 1 \"%1\"\n").arg(p1.at(12)));
    text.append(QString("TO 0 10 1 2 \"%1\"\n").arg(p1.at(9)));
    text.append(QString("TO 0 18 1 0 \"%1\"\n").arg(p2.at(1)));
    text.append(QString("TO 0 18 1 1 \"%1\"\n").arg(p2.at(12)));
    text.append(QString("TO 0 18 1 2 \"%1\"\n").arg(p2.at(9)));
    text.append(QString("TO 0 26 1 0 \"%1\"\n").arg(p3.at(1)));
    text.append(QString("TO 0 26 1 1 \"%1\"\n").arg(p3.at(12)));
    text.append(QString("TO 0 26 1 2 \"%1\"\n").arg(p3.at(9)));
    text.append(QString("TO 0 34 1 0 \"%1\"\n").arg(p4.at(1)));
    text.append(QString("TO 0 34 1 1 \"%1\"\n").arg(p4.at(12)));
    text.append(QString("TO 0 34 1 2 \"%1\"\n").arg(p4.at(9)));
    text.append("MC 0\n");

    sendComposer(text);
}
