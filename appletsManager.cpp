#include "appletsManager.h"

#include "applets/amarokapplet.h"
#include "applets/audaciousapplet.h"
#include "applets/clementineapplet.h"
#include "applets/exaileapplet.h"
#include "applets/hardwareapplet.h"
#include "applets/processesapplet.h"
#include "applets/chronoapplet.h"


AppletsManager::AppletsManager() {

    applets = std::vector < std::pair<bool,Applet*> > (N_APPLETS);

    for (int i = 0; i < N_APPLETS; ++i) applets[i].first = false;
}

bool AppletsManager::toggleApplet(int n) {

    if (applets[n].first) {
        delete(applets[n].second);
        applets[n].first = false;
        return true;
    }
    else {

        switch(n) {
            case APPLET_AMAROK:
                applets[n].second = new amarokApplet();
                break;

            case APPLET_AUDACIOUS:
                applets[n].second = new audaciousApplet();
                break;

            case APPLET_CLEMENTINE:
                applets[n].second = new clementineApplet();
                break;

            case APPLET_EXAILE:
                applets[n].second = new exaileApplet();
                break;

            case APPLET_HARDWARE:
                applets[n].second = new hardwareApplet();
                break;

            case APPLET_TOP:
                applets[n].second = new processesApplet();
                break;

            case APPLET_CHRONO:
                applets[n].second = new chronoApplet();
                break;
        }

        if(applets[n].second->init()) {
            applets[n].first = true;
            return true;
        }
        else {
            delete(applets[n].second);
            return false;
        }

    }
}


void AppletsManager::update() {
    for (int i = 0; i < N_APPLETS; ++i) {
        if (applets[i].first) applets[i].second->update();
    }
}
