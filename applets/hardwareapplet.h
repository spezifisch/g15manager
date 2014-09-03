#ifndef HARDWAREAPPLET_H
#define HARDWAREAPPLET_H

#include "applet.h"

class hardwareApplet : public Applet
{
    public:
        hardwareApplet();
        void update();

    private:
        int cpuOld;
        int idleOld;
};

#endif // HARDWAREAPPLET_H
