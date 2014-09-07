#ifndef GMAILAPPLET_H
#define GMAILAPPLET_H

#include "applet.h"

class gmailApplet : public Applet
{
    public:
        gmailApplet();
        ~gmailApplet();

        void update();
};

#endif // GMAILAPPLET_H
