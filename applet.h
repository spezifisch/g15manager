#ifndef APPLET_H
#define APPLET_H

#include <QString>
#include <QProcess>

class Applet {
    public:
        Applet();
        virtual ~Applet();

        virtual void update();

        void killComposer();

    protected:
        QString name;
        QProcess *composer;
        void startComposer();
        void sendComposer(QString text);
        static QString eliminarAccents(QString t);
};

#endif // APPLET_H
