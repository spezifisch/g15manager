#include <QApplication>
#include <QTimer>
#include <iostream>

#include "mainwindow.h"

int main(int argc, char *argv[]) {

    bool hide = false;

    QApplication a(argc, argv);
    a.setOrganizationName("G15Manager");

    QSettings settings;

    if (argc > 1) {
        if (QString(argv[1]) == "--autostart") {
            if (not settings.value("autostart", true).toBool()) exit(0);
         }
        else if (QString(argv[1]) == "--hide") hide = true;
        else {
            std::cout << "G15 Manager Help" << std::endl
                         << "--autostart: The program only starts if the autostart option is activated." << std::endl
                         << "--hide: The program starts hidden." << std::endl
                         << "--help: This help." << std::endl << std::endl;
            exit(0);
        }
    }

    MainWindow w;

    QTimer timer;
    a.connect(&timer, SIGNAL(timeout()), &w, SLOT(timer()));
    timer.start(950);


    if (not hide and not settings.value("start_hidden", true).toBool()) w.show();

    return a.exec();
}
