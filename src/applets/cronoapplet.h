#ifndef CRONOAPPLET_H
#define CRONOAPPLET_H


#include "applet.h"

#define STOPPED 0
#define RUNNING 1
#define PAUSED 2
#define SET_M 3
#define SET_S 4
#define FINISHED 5

class cronoApplet :  public Applet
{
    public:
        cronoApplet();
        ~cronoApplet();

        void update();

    private:
        bool countdown;
        int state;

        int set_time;

        int time;

        bool blink;
};

#endif // CRONOAPPLET_H
