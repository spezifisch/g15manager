#ifndef RHYTHMBOXAPPLET_H
#define RHYTHMBOXAPPLET_H

#include "applet.h"

class rhythmboxApplet : public Applet
{
    public:
        rhythmboxApplet();
        ~rhythmboxApplet();

        void update();
};

#endif // RHYTHMBOXAPPLET_H
