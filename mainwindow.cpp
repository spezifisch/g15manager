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

    QIcon icon = QIcon("/usr/share/g15manager/icons/g15_24.png");
    trayIcon = new QSystemTrayIcon(icon, this);
    trayIcon->setContextMenu(trayMenu);
    connect(trayIcon, SIGNAL(activated(QSystemTrayIcon::ActivationReason)), this, SLOT(trayIconClick(QSystemTrayIcon::ActivationReason)));
    trayIcon->show();

    tancar = false;

    QSettings settings;

    ui->button_Amarok->setChecked(settings.value("amarok", false).toBool());
    ui->button_Audacious->setChecked(settings.value("audacious", false).toBool());
    ui->button_Clementine->setChecked(settings.value("clementine", false).toBool());
    ui->button_Exaile->setChecked(settings.value("exaile", false).toBool());
    ui->button_Hard->setChecked(settings.value("hardware", false).toBool());
    ui->button_Top->setChecked(settings.value("top", false).toBool());
    ui->button_Chrono->setChecked(settings.value("chrono", false).toBool());

    ui->checkStartHidden->setChecked(settings.value("start_hidden", true).toBool());
    ui->checkAutostart->setChecked(settings.value("autostart", true).toBool());
}


MainWindow::~MainWindow() {
    settings.setValue("amarok", ui->button_Amarok->isChecked());
    settings.setValue("audacious", ui->button_Audacious->isChecked());
    settings.setValue("clementine", ui->button_Clementine->isChecked());
    settings.setValue("exaile", ui->button_Exaile->isChecked());
    settings.setValue("hardware", ui->button_Hard->isChecked());
    settings.setValue("top", ui->button_Top->isChecked());
    settings.setValue("chrono", ui->button_Chrono->isChecked());

    settings.setValue("start_hidden", ui->checkStartHidden->isChecked());
    settings.setValue("autostart", ui->checkAutostart->isChecked());

    settings.sync();

    delete ui;
}

void MainWindow::closeApp(){
    tancar = true;
    close();
}


void MainWindow::trayIconClick(QSystemTrayIcon::ActivationReason reason) {

    if (reason == QSystemTrayIcon::Trigger) {
        if (this->isVisible()) this->hide();
        else this->show();
    }
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
    if (!applets.toggleApplet(APPLET_AMAROK)) ui->button_Amarok->setChecked(false);
}

void MainWindow::on_button_Audacious_toggled()
{
    if (!applets.toggleApplet(APPLET_AUDACIOUS)) ui->button_Audacious->setChecked(false);
}

void MainWindow::on_button_Clementine_toggled()
{
    if (!applets.toggleApplet(APPLET_CLEMENTINE)) ui->button_Clementine->setChecked(false);
}

void MainWindow::on_button_Exaile_toggled()
{
    if (!applets.toggleApplet(APPLET_EXAILE)) ui->button_Exaile->setChecked(false);
}

void MainWindow::on_button_Hard_toggled()
{
    if (!applets.toggleApplet(APPLET_HARDWARE)) ui->button_Hard->setChecked(false);
}

void MainWindow::on_button_Top_toggled()
{
    if (!applets.toggleApplet(APPLET_TOP)) ui->button_Top->setChecked(false);
}

void MainWindow::on_button_Chrono_toggled()
{
    if (!applets.toggleApplet(APPLET_CHRONO)) ui->button_Chrono->setChecked(false);
}
