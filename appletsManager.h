#ifndef APPLETSMANAGER_H
#define APPLETSMANAGER_H

#include <vector>

#include "applets/applet.h"

#define APPLET_AMAROK 0
#define APPLET_AUDACIOUS 1
#define APPLET_EXAILE 2
#define APPLET_CLEMENTINE 3
#define APPLET_GMAIL 4
#define APPLET_HARDWARE 5
#define APPLET_TOP 6


class AppletsManager {

    public:
        AppletsManager();

        void toggleApplet(int n);

        void update();

    private:
        std::vector < std::pair<bool,Applet*> > applets;

};



#endif
