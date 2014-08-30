#include "hardwareapplet.h"

hardwareApplet::hardwareApplet() : Applet() {
    name = "hardware";
    startComposer();
}


void hardwareApplet::update() {
    sendComposer("MC 1\nPC 0\nTO 0 2 1 1 \"Title\"\nMC 0\n");
}
