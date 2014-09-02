#include <QDebug>

#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui->setupUi(this);


    trayMenu = new QMenu(this);

    QAction *showTray = new QAction("Show", this);
    connect(showTray, SIGNAL(triggered()), this, SLOT(show()));
    trayMenu->addAction(showTray);

    trayMenu->addSeparator();

    QAction *closeTray = new QAction("Close", this);
    connect(closeTray, SIGNAL(triggered()), this, SLOT(closeApp()));
    trayMenu->addAction(closeTray);

    QIcon icon = QIcon("icons/g15_24.png");
    trayIcon = new QSystemTrayIcon(icon, this);
    trayIcon->setContextMenu(trayMenu);
    trayIcon->show();

    tancar = false;
}

void MainWindow::closeApp(){
    tancar = true;
    close();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::timer()
{
    applets.update();
}


void MainWindow::closeEvent(QCloseEvent *event) {
    if (not tancar) {
        event->ignore();
        hide();
    }
}

void MainWindow::on_button_Amarok_clicked()
{
    applets.toggleApplet(APPLET_AMAROK);
}

void MainWindow::on_button_Audacious_clicked()
{
    applets.toggleApplet(APPLET_AUDACIOUS);
}

void MainWindow::on_button_Clementine_clicked()
{
    applets.toggleApplet(APPLET_CLEMENTINE);
}

void MainWindow::on_button_Exaile_clicked()
{
    applets.toggleApplet(APPLET_EXAILE);
}

void MainWindow::on_button_Gmail_clicked()
{
    applets.toggleApplet(APPLET_GMAIL);
}

void MainWindow::on_button_Hard_clicked()
{
    applets.toggleApplet(APPLET_HARDWARE);
}

void MainWindow::on_button_Top_clicked()
{
    applets.toggleApplet(APPLET_TOP);
}
