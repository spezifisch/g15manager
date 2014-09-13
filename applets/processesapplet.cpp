#include <QProcess>

#include "processesapplet.h"

processesApplet::processesApplet() : Applet() {}

processesApplet::~processesApplet() {}

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
    procs.append(linies.at(11));

    QStringList p1 = procs.at(0).split(QRegExp("\\s+"));
    QStringList p2 = procs.at(1).split(QRegExp("\\s+"));
    QStringList p3 = procs.at(2).split(QRegExp("\\s+"));
    QStringList p4 = procs.at(3).split(QRegExp("\\s+"));
    QStringList p5 = procs.at(4).split(QRegExp("\\s+"));

    if (p1.first() == "") p1.erase(p1.begin());
    if (p2.first() == "") p2.erase(p2.begin());
    if (p3.first() == "") p3.erase(p3.begin());
    if (p4.first() == "") p4.erase(p4.begin());
    if (p5.first() == "") p5.erase(p5.begin());

    g15r_clearScreen(canvas, 0);

    g15r_G15FPrint(canvas, (char *) "Process Monitor", 0, 0, 1, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 0);

    g15r_G15FPrint(canvas, qstringToChar(p1.at(0)), 0, 0, 0, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 2);
    g15r_G15FPrint(canvas, qstringToChar(p2.at(0)), 0, 0, 0, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 3);
    g15r_G15FPrint(canvas, qstringToChar(p3.at(0)), 0, 0, 0, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 4);
    g15r_G15FPrint(canvas, qstringToChar(p4.at(0)), 0, 0, 0, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 5);
    g15r_G15FPrint(canvas, qstringToChar(p5.at(0)), 0, 0, 0, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 6);

    g15r_G15FPrint(canvas, qstringToChar(p1.at(11)), 0, 0, 0, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 2);
    g15r_G15FPrint(canvas, qstringToChar(p2.at(11)), 0, 0, 0, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 3);
    g15r_G15FPrint(canvas, qstringToChar(p3.at(11)), 0, 0, 0, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 4);
    g15r_G15FPrint(canvas, qstringToChar(p4.at(11)), 0, 0, 0, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 5);
    g15r_G15FPrint(canvas, qstringToChar(p5.at(11)), 0, 0, 0, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 6);

    g15r_G15FPrint(canvas, qstringToChar(p1.at(9)), 0, 0, 0, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 2);
    g15r_G15FPrint(canvas, qstringToChar(p2.at(9)), 0, 0, 0, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 3);
    g15r_G15FPrint(canvas, qstringToChar(p3.at(9)), 0, 0, 0, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 4);
    g15r_G15FPrint(canvas, qstringToChar(p4.at(9)), 0, 0, 0, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 5);
    g15r_G15FPrint(canvas, qstringToChar(p5.at(9)), 0, 0, 0, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 6);

    g15_send(fd, (char *) canvas->buffer, G15_BUFFER_LEN);
}
