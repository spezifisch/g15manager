#include "applet.h"
#include <QRegExp>
#include <QDebug>

Applet::Applet() {
    fd = new_g15_screen(G15_G15RBUF);
    canvas = (g15canvas *) malloc(sizeof(g15canvas));

    memset(canvas->buffer, 0, G15_BUFFER_LEN);
    canvas->mode_cache = 0;
    canvas->mode_reverse = 0;
    canvas->mode_xor = 0;

    screen = 0;
}

Applet::~Applet() {
    g15_close_screen(fd);
}

void Applet::update() {}


QString Applet::eliminarAccents(QString t) {
    return t.normalized(QString::NormalizationForm_D).replace(QRegExp("[^a-zA-Z\\s]"), "");
}

char *Applet::qstringToChar(QString s) {

    char *aux = (char *) s.toStdString().c_str();
    return aux;
}
