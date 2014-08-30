#include <QApplication>
#include <QTimer>

#include "mainwindow.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    MainWindow w;

    QTimer timer;
    a.connect(&timer, SIGNAL(timeout()), &w, SLOT(timer()));
    timer.start(900);

    w.show();

    return a.exec();
}