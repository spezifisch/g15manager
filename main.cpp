#include <QApplication>
#include <QTimer>

#include "mainwindow.h"

int main(int argc, char *argv[]) {

    QApplication a(argc, argv);
    a.setOrganizationName("G15Manager");

    MainWindow w;

    QTimer timer;
    a.connect(&timer, SIGNAL(timeout()), &w, SLOT(timer()));
    timer.start(900);

    return a.exec();

}
