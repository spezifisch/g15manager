#ifndef APPLET_H
#define APPLET_H

#include <QString>

#include <g15daemon_client.h>
#include <libg15render.h>

class Applet {
    public:
        Applet();
        ~Applet();

        virtual void update();

    protected:

        int fd;
        g15canvas *canvas;

        static QString eliminarAccents(QString t);
        static char *qstringToChar(QString s);
};

#endif // APPLET_H
