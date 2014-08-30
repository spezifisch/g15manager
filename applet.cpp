#include <QProcess>
#include <QFile>
#include <QTextStream>
#include <QString>
#include <QStringList>

#include "applet.h"
using namespace std;

Applet::Applet() {}
Applet::~Applet() {}

void Applet::update() {}


void Applet::startComposer() {
    composer = new QProcess(0);

    QString program = "g15composer";
    QStringList arguments;

    arguments.append("/tmp/g15manager-"+name);

    composer->start(program, arguments);
}


void Applet::killComposer() {

    composer->kill();
    QFile::remove("/tmp/g15manager-"+name);
}

void Applet::sendComposer(QString text) {
    QFile file("/tmp/g15manager-"+name);
    file.open(QIODevice::WriteOnly | QIODevice::Text);

    QTextStream out(&file);
    out << text;
    file.close();
}

QString Applet::eliminarAccents(QString t) {
    return t.normalized(QString::NormalizationForm_D).replace(QRegExp("[^a-zA-Z\\s]"), "");
}
