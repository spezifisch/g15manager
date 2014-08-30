#ifndef APPLETSMANAGER_H
#define APPLETSMANAGER_H

#include <vector>

#include "applet.h"
using namespace std;

class AppletsManager {

    public:
        AppletsManager();

        void toggleApplet(int n);

        void update();

    private:
        vector < pair<bool,Applet*> > applets;

};



#endif
