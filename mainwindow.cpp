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

void MainWindow::on_checkBox_1_toggled(bool checked)
{
    applets.toggleApplet(0);
}

void MainWindow::on_checkBox_2_toggled(bool checked)
{
    applets.toggleApplet(1);
}

void MainWindow::on_checkBox_3_toggled(bool checked)
{
    applets.toggleApplet(2);
}

void MainWindow::on_checkBox_4_toggled(bool checked)
{
    applets.toggleApplet(3);
}

void MainWindow::on_checkBox_5_toggled(bool checked)
{
    applets.toggleApplet(4);
}

void MainWindow::on_checkBox_6_toggled(bool checked)
{
    applets.toggleApplet(5);
}

void MainWindow::on_checkBox_7_toggled(bool checked)
{
    applets.toggleApplet(6);
}

void MainWindow::closeEvent(QCloseEvent *event) {
    if (not tancar) {
        event->ignore();
        hide();
    }
}
