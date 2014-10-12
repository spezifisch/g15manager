#include <sys/socket.h>
#include <QDebug>

#include "chronoapplet.h"

chronoApplet::chronoApplet() : Applet() {
    countdown = false;

    time = 0;
    set_time = 0;

    state = STOPPED;

    blink = false;

}

chronoApplet::~chronoApplet() {}

void chronoApplet::update() {

    if (!blink) g15r_clearScreen(canvas, G15_COLOR_WHITE);
    else g15r_clearScreen(canvas, G15_COLOR_BLACK);

    if (state == RUNNING) {
        if (countdown) {
            if (time == 0) state = FINISHED;
            else --time;
        }
        else ++time;
    }

    unsigned int keystate = 0;

    while (recv(fd, &keystate, 4, 0) > 0) {

        if (keystate) {
            if (keystate & G15_KEY_L2) {
                if (state == STOPPED) countdown = !countdown;
                else if (state == SET_M) set_time += 60;
                else if (state == SET_S) ++set_time;
                else if (state == FINISHED) {
                    canvas->mode_reverse = 0;
                    blink = false;
                    state = STOPPED;
                    time = 0;
                }
            }
            else if (keystate & G15_KEY_L3) {
                if (state == STOPPED) state = SET_M;
                else if (state == RUNNING) state = PAUSED;
                else if (state == PAUSED) state = RUNNING;
                else if (state == SET_M && set_time > 59) set_time -= 60;
                else if (state == SET_S && set_time > 0) --set_time;
                else if (state == FINISHED) {
                    canvas->mode_reverse = 0;
                    blink = false;
                    if (countdown) time = set_time;
                    else time = 0;
                    state = RUNNING;
                }
            }
            else if (keystate & G15_KEY_L4) {
                if (state == STOPPED) {
                    state = RUNNING;
                    if (countdown) time = set_time;
                }
                else if (state == RUNNING) state = FINISHED;
                else if (state == PAUSED) state = FINISHED;
                else if (state == SET_M) state = SET_S;
                else if (state == SET_S) state = SET_M;
            }
            else if (keystate & G15_KEY_L5) {
                if (state == SET_M) state = STOPPED;
                else if (state == SET_S) state = STOPPED;
            }
        }
    }


    if (countdown) g15r_G15FPrint(canvas, (char *) "COUNTDOWN", 0, 1, G15_TEXT_MED, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 0);
    else g15r_G15FPrint(canvas, (char *) "CHRONOMETER", 0, 1, G15_TEXT_MED, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 0);

    if (state == SET_M || state == SET_S) time = set_time;
    QString strtime;
    if (time/60 < 10) strtime.append("0");
    strtime.append(QString::number(time/60));
    strtime.append(":");
    if (time%60 < 10) strtime.append("0");
    strtime.append(QString::number(time%60));

    g15r_G15FPrint(canvas, (char *) strtime.toStdString().c_str(), 0, 2, G15_TEXT_HUGE, G15_JUSTIFY_CENTER, G15_COLOR_BLACK, 1);


    if (state == STOPPED && countdown) g15r_G15FPrint(canvas, (char *) " MODE     SET     START", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 5);
    else if (state == STOPPED && !countdown) g15r_G15FPrint(canvas, (char *) " MODE             START", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 5);
    else if (state == RUNNING) g15r_G15FPrint(canvas, (char *) "         PAUSE    STOP", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 5);
    else if (state == PAUSED) g15r_G15FPrint(canvas, (char *) "         RESUME   STOP", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 5);
    else if (state == SET_M) g15r_G15FPrint(canvas, (char *) "   +      -      SECONDS    OK", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 5);
    else if (state == SET_S) g15r_G15FPrint(canvas, (char *) "   +      -      MINUTES    OK", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 5);
    else if (state == FINISHED) {
        g15r_G15FPrint(canvas, (char *) " EXIT   RESTART", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 5);
        blink = !blink;
        if (blink) canvas->mode_reverse = 1;
        else canvas->mode_reverse = 0;
    }

    g15_send(fd, (char *) canvas->buffer, G15_BUFFER_LEN);
}

