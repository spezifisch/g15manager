#include <QApplication>
#include <QTimer>

#include "mainwindow.h"

int main(int argc, char *argv[]) {

    QApplication a(argc, argv);
    a.setOrganizationName("G15Manager");

    MainWindow w;

    QTimer timer;
    a.connect(&timer, SIGNAL(timeout()), &w, SLOT(timer()));
    timer.start(950);

    QSettings settings;

    if (not (argc > 1 and QString(argv[1]) == "--hide") and not settings.value("start_hidden", false).toBool()) w.show();

    return a.exec();
}
