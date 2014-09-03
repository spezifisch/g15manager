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

    QSettings settings;

    ui->button_Amarok->setChecked(settings.value("amarok", false).toBool());
    ui->button_Audacious->setChecked(settings.value("audacious", false).toBool());
    ui->button_Clementine->setChecked(settings.value("clementine", false).toBool());
    ui->button_Exaile->setChecked(settings.value("exaile", false).toBool());
    ui->button_Gmail->setChecked(settings.value("gmail", false).toBool());
    ui->button_Hard->setChecked(settings.value("hardware", false).toBool());
    ui->button_Top->setChecked(settings.value("top", false).toBool());



    if (settings.value("start_hidden", false).toBool()) {
        ui->checkStartHidden->setChecked(true);
    }
    else show();

}

MainWindow::~MainWindow() {
    settings.setValue("amarok", ui->button_Amarok->isChecked());
    settings.setValue("audacious", ui->button_Audacious->isChecked());
    settings.setValue("clementine", ui->button_Clementine->isChecked());
    settings.setValue("exaile", ui->button_Exaile->isChecked());
    settings.setValue("gmail", ui->button_Gmail->isChecked());
    settings.setValue("hardware", ui->button_Hard->isChecked());
    settings.setValue("top", ui->button_Top->isChecked());


    settings.setValue("start_hidden", ui->checkStartHidden->isChecked());

    settings.sync();

    delete ui;
}

void MainWindow::closeApp(){
    tancar = true;
    close();
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

void MainWindow::on_button_Amarok_toggled()
{
    applets.toggleApplet(APPLET_AMAROK);
}

void MainWindow::on_button_Audacious_toggled()
{
    applets.toggleApplet(APPLET_AUDACIOUS);
}

void MainWindow::on_button_Clementine_toggled()
{
    applets.toggleApplet(APPLET_CLEMENTINE);
}

void MainWindow::on_button_Exaile_toggled()
{
    applets.toggleApplet(APPLET_EXAILE);
}

void MainWindow::on_button_Gmail_toggled()
{
    applets.toggleApplet(APPLET_GMAIL);
}

void MainWindow::on_button_Hard_toggled()
{
    applets.toggleApplet(APPLET_HARDWARE);
}

void MainWindow::on_button_Top_toggled()
{
    applets.toggleApplet(APPLET_TOP);
}

