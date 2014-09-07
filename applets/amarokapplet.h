#ifndef AMAROKAPPLET_H
#define AMAROKAPPLET_H

#include "applet.h"

class amarokApplet : public Applet
{
    public:
        amarokApplet();
        ~amarokApplet();

        void update();
};

#endif // AMAROKAPPLET_H
