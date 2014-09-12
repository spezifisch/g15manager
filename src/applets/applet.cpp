#include "applet.h"
#include <QRegExp>

Applet::Applet() {}

bool Applet::init() {
    fd = new_g15_screen(G15_G15RBUF);
    if (fd < 0) return false;

    canvas = (g15canvas *) malloc(sizeof(g15canvas));

    memset(canvas->buffer, 0, G15_BUFFER_LEN);
    canvas->mode_cache = 0;
    canvas->mode_reverse = 0;
    canvas->mode_xor = 0;

    screen = 0;

    return true;
  }

Applet::~Applet() {
    if (fd > 0) g15_close_screen(fd);
}

void Applet::update() {}


QString Applet::eliminarAccents(QString t) {
    return t.normalized(QString::NormalizationForm_D).replace(QRegExp("[^a-zA-Z0-9\\s-:!¡?¿]"), "");
}

char *Applet::qstringToChar(QString s) {

    char *aux = (char *) s.toStdString().c_str();
    return aux;
}
