#include "hardwareapplet.h"
#include <QFile>
#include <QStringList>
#include <QRegExp>
#include <QDebug>

hardwareApplet::hardwareApplet() : Applet() {

    cpuOld = 0;
    idleOld = 0;
}

void hardwareApplet::update() {
    g15r_clearScreen(canvas, 0);



    QFile file("/proc/stat");

    //CPU
    file.open(QIODevice::ReadOnly);
    QStringList strcpu = QString(file.readLine()).split(QRegExp("\\s+"));
    file.close();

    int cpu = strcpu.at(1).toInt() + strcpu.at(2).toInt() + strcpu.at(3).toInt() + strcpu.at(5).toInt();
    float diffCpu = cpu - cpuOld;
    cpuOld = cpu;

    int idle = strcpu.at(4).toInt();
    int diffIdle = idle - idleOld;
    idleOld = idle;

    int progressCpu =  diffCpu/(diffCpu+diffIdle)*128;


    //MEM
    file.setFileName("/proc/meminfo");
    file.open(QIODevice::ReadOnly);
    QStringList memL1 = QString(file.readLine()).split(QRegExp("\\s+"));
    QStringList memL2 = QString(file.readLine()).split(QRegExp("\\s+"));
    file.close();

    int progressMem = memL2.at(1).toFloat()/memL1.at(1).toInt()*128;

    unsigned int key_state = 0;

/*    int ret = getPressedKeys(&key_state, 100);
    if (!ret == G15_ERROR_TRY_AGAIN) {


    qDebug() << "Getting key states: " << ret << endl;
    qDebug() << "Key state: " << key_state << endl;
    qDebug() << "Pressed Keys: " ;
    if (key_state & G15_KEY_L3) qDebug() << "L3 ";
    if (key_state & G15_KEY_L4) qDebug() << "L4 ";
    }
*/


    g15r_G15FPrint(canvas, (char *) " CPU", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 1);
    g15r_pixelBox(canvas, 28, 7, 28+progressCpu, 12, G15_COLOR_BLACK, 1, G15_PIXEL_FILL);
    g15r_pixelBox(canvas, 28+progressCpu, 7, 156, 12, G15_COLOR_BLACK, 1, G15_PIXEL_NOFILL);

    g15r_G15FPrint(canvas, (char *) " MEM", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 3);
    g15r_pixelBox(canvas, 28, 21, 28+progressMem, 26, G15_COLOR_BLACK, 1, G15_PIXEL_FILL);
    g15r_pixelBox(canvas, 28+progressMem, 21, 156, 26, G15_COLOR_BLACK, 1, G15_PIXEL_NOFILL);

    //g15r_G15FPrint(canvas, (char *) " ALL      CPU      MEM      NET", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 5);

    g15_send(fd, (char *) canvas->buffer, G15_BUFFER_LEN);
}
