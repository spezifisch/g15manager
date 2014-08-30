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
    void on_checkBox_1_toggled(bool checked);
    void on_checkBox_2_toggled(bool checked);
    void on_checkBox_3_toggled(bool checked);
    void on_checkBox_4_toggled(bool checked);
    void on_checkBox_5_toggled(bool checked);
    void on_checkBox_6_toggled(bool checked);
    void on_checkBox_7_toggled(bool checked);
    void closeApp();

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
