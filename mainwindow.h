#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QMenu>
#include <QAction>
#include <QSystemTrayIcon>
#include <QCloseEvent>
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

    void on_button_Amarok_clicked();
    void on_button_Audacious_clicked();
    void on_button_Clementine_clicked();
    void on_button_Exaile_clicked();
    void on_button_Gmail_clicked();
    void on_button_Hard_clicked();
    void on_button_Top_clicked();

private:
    Ui::MainWindow *ui;
    AppletsManager applets;

    QSystemTrayIcon *trayIcon;
    QMenu *trayMenu;

    QApplication *app;

    void closeEvent(QCloseEvent *event);

    bool tancar;
};

#endif // MAINWINDOW_H
