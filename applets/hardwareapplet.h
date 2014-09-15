#ifndef HARDWAREAPPLET_H
#define HARDWAREAPPLET_H

#include "applet.h"

class hardwareApplet : public Applet
{
    public:
        hardwareApplet();
        ~hardwareApplet();

        void update();

    private:
        int cpuOld;
        int idleOld;

        int recvBytesOld;
        int transBytesOld;
};

#endif // HARDWAREAPPLET_H
