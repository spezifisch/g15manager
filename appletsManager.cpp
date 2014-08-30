#include <vector>
#include <QDebug>
#include "appletsManager.h"

#include "amarokapplet.h"
#include "audaciousapplet.h"
#include "clementineapplet.h"
#include "exaileapplet.h"
#include "gmailapplet.h"
#include "hardwareapplet.h"
#include "processesapplet.h"
#include "rhythmboxapplet.h"

using namespace std;

AppletsManager::AppletsManager() {

    applets = vector < pair<bool,Applet*> > (8);

    for (int i = 0; i < 8; ++i) applets[i].first = false;
}

void AppletsManager::toggleApplet(int n) {

    if (applets[n].first) applets[n].second->killComposer();
    else {

        switch(n) {
            case 0:
                applets[n].second = new amarokApplet();
                break;

            case 1:
                applets[n].second = new audaciousApplet();
                break;

            case 2:
                applets[n].second = new clementineApplet();
                break;

            case 3:
                applets[n].second = new exaileApplet();
                break;

            case 4:
                applets[n].second = new gmailApplet();
                break;

            case 5:
                applets[n].second = new hardwareApplet();
                break;

            case 6:
                applets[n].second = new processesApplet();
                break;

            case 7:
                applets[n].second = new rhythmboxApplet();
                break;
        }
    }

    applets[n].first = !applets[n].first;
}


void AppletsManager::update() {
    for (int i = 0; i < 8; ++i) {
        if (applets[i].first) applets[i].second->update();
    }
}
