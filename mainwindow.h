#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QMenu>
#include <QAction>
#include <QSystemTrayIcon>
#include <QCloseEvent>
#include <QSettings>
#include "appletsManager.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();



private slots:
    void timer();

    void closeApp();

    void trayIconClick(QSystemTrayIcon::ActivationReason reason);

    void on_button_Amarok_toggled();
    void on_button_Audacious_toggled();
    void on_button_Clementine_toggled();
    void on_button_Exaile_toggled();
    void on_button_Hard_toggled();
    void on_button_Top_toggled();
    void on_button_Chrono_toggled();

private:
    Ui::MainWindow *ui;
    AppletsManager applets;

    QSystemTrayIcon *trayIcon;
    QMenu *trayMenu;

    QApplication *app;

    void closeEvent(QCloseEvent *event);

    bool tancar;

    QSettings settings;
};

#endif // MAINWINDOW_H
