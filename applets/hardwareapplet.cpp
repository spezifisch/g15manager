#include "hardwareapplet.h"
#include <QFile>
#include <QStringList>
#include <QRegExp>
#include <QDebug>

#include <cmath>
#include <sys/socket.h>


hardwareApplet::hardwareApplet() : Applet() {

    cpuOld = 0;
    idleOld = 0;

    recvBytesOld = 0;
    transBytesOld = 0;
}

hardwareApplet::~hardwareApplet() {}

void hardwareApplet::update() {

    g15r_clearScreen(canvas, 0);

    unsigned int keystate = 0;

    recv(fd, &keystate, 4, 0);

    if (keystate) {
        if (keystate & G15_KEY_L2) screen = 0;
        else if (keystate & G15_KEY_L3) screen = 1;
        else if (keystate & G15_KEY_L4) screen = 2;
        else if (keystate & G15_KEY_L5) screen = 3;
    }

    QFile file;

    if (screen == 0) {

        //CPU
        file.setFileName("/proc/stat");
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

        int progressMem = (memL1.at(1).toInt()-memL2.at(1).toInt())/memL1.at(1).toFloat()*128;


        g15r_G15FPrint(canvas, (char *) " CPU", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 1);
        g15r_pixelBox(canvas, 28, 7, 28+progressCpu, 12, G15_COLOR_BLACK, 1, G15_PIXEL_FILL);
        g15r_pixelBox(canvas, 28+progressCpu, 7, 156, 12, G15_COLOR_BLACK, 1, G15_PIXEL_NOFILL);

        g15r_G15FPrint(canvas, (char *) " MEM", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 3);
        g15r_pixelBox(canvas, 28, 21, 28+progressMem, 26, G15_COLOR_BLACK, 1, G15_PIXEL_FILL);
        g15r_pixelBox(canvas, 28+progressMem, 21, 156, 26, G15_COLOR_BLACK, 1, G15_PIXEL_NOFILL);
    }

    //CPU
    else if (screen == 1) {
        file.setFileName("/proc/stat");
        file.open(QIODevice::ReadOnly);
        QStringList strcpu = QString(file.readLine()).split(QRegExp("\\s+"));
        file.close();

        int user = strcpu.at(1).toInt();
        int nice = strcpu.at(2).toInt();
        int sys = strcpu.at(3).toInt();
        int idle = strcpu.at(4).toInt();


        float diffUser = user - userOld;
        float diffNice = nice - niceOld;
        float diffSys = sys - sysOld;
        float diffIdle = idle - idleOld;
        float diffTotal = diffUser + diffNice + diffSys + diffIdle;

        userOld = user;
        niceOld = nice;
        sysOld = sys;
        idleOld = idle;


        QString progressUser = QString::number(std::floor(diffUser/diffTotal*10000)/100).append(" %         ");
        QString progressNice = QString::number(std::floor(diffNice/diffTotal*10000)/100).append(" %         ");
        QString progressSys =  QString::number(std::floor(diffSys/diffTotal*10000)/100).append(" %         ");
        QString progressCpu =  QString::number(std::floor((diffUser + diffNice + diffSys)/diffTotal*10000)/100).append(" %         ");



        g15r_G15FPrint(canvas, (char *) "  User :", 24, 4, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 0);
        g15r_G15FPrint(canvas, (char *) "  Nice :", 24, 4, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 1);
        g15r_G15FPrint(canvas, (char *) "System :", 24, 4, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 2);
        g15r_G15FPrint(canvas, (char *) " Total :", 24, 4, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 3);


        g15r_G15FPrint(canvas, (char *) progressUser.toStdString().c_str(), 0, 4, 1, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 0);
        g15r_G15FPrint(canvas, (char *) progressNice.toStdString().c_str(), 0, 4, 1, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 1);
        g15r_G15FPrint(canvas, (char *) progressSys.toStdString().c_str(), 0, 4, 1, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 2);
        g15r_G15FPrint(canvas, (char *) progressCpu.toStdString().c_str(), 0, 4, 1, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 3);

    }

    //MEM
    else if (screen == 2) {
        file.setFileName("/proc/meminfo");
        file.open(QIODevice::ReadOnly);

        float MemTotal = QString(file.readLine()).split(QRegExp("\\s+"))[1].toInt();
        int MemFree = QString(file.readLine()).split(QRegExp("\\s+"))[1].toInt();
        int Buffers = QString(file.readLine()).split(QRegExp("\\s+"))[1].toInt();
        int Cached = QString(file.readLine()).split(QRegExp("\\s+"))[1].toInt();

        file.close();

        int progressTotal = 31 + (MemTotal-MemFree)/MemTotal*125;
        int progressUsr = 31 + (MemTotal-MemFree-Buffers-Cached)/MemTotal*125;
        int progressBuffers = progressUsr + Buffers/MemTotal*125;
        int progressCached = progressBuffers + Cached/MemTotal*125;


        g15r_G15FPrint(canvas, (char *) " TOTAL", 2, 2, 0, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 0);
        g15r_pixelBox(canvas, 31, 2, progressTotal, 6, G15_COLOR_BLACK, 1, G15_PIXEL_FILL);
        g15r_pixelBox(canvas, progressTotal, 2, 156, 6, G15_COLOR_BLACK, 1, G15_PIXEL_NOFILL);

        g15r_G15FPrint(canvas, (char *) " USER", 4, 4, 0, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 1);
        g15r_pixelBox(canvas, 31, 10, progressUsr, 14, G15_COLOR_BLACK, 1, G15_PIXEL_FILL);
        g15r_pixelBox(canvas, progressUsr, 10, 156, 14, G15_COLOR_BLACK, 1, G15_PIXEL_NOFILL);

        g15r_G15FPrint(canvas, (char *) "BUFFERS", 2, 0, 0, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 3);
        g15r_pixelBox(canvas, 31, 18, progressUsr+1, 22, G15_COLOR_BLACK, 1, G15_PIXEL_NOFILL);
        g15r_pixelBox(canvas, progressUsr+1, 18, progressBuffers, 22, G15_COLOR_BLACK, 1, G15_PIXEL_FILL);
        g15r_pixelBox(canvas, progressBuffers, 18, 156, 22, G15_COLOR_BLACK, 1, G15_PIXEL_NOFILL);

        g15r_G15FPrint(canvas, (char *) "CACHED", 3, 2, 0, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 4);
        g15r_pixelBox(canvas, 31, 26, progressBuffers+1, 30, G15_COLOR_BLACK, 1, G15_PIXEL_NOFILL);
        g15r_pixelBox(canvas, progressBuffers+1, 26, progressCached, 30, G15_COLOR_BLACK, 1, G15_PIXEL_FILL);
        g15r_pixelBox(canvas, progressCached, 26, 156, 30, G15_COLOR_BLACK, 1, G15_PIXEL_NOFILL);
    }

    
    //NET
    else if (screen == 3) {
        file.setFileName("/proc/net/dev");
        file.open(QIODevice::ReadOnly);
        
        int recvBytes = 0;
        int transBytes = 0;

        file.readLine();
        file.readLine();

        while (file.canReadLine()) {
            QStringList line = QString(file.readLine()).split(QRegExp("\\s+"));

            if (line.at(1) != "lo:") {
                recvBytes += line.at(2).toInt();
                transBytes += line.at(10).toInt();
            }
        }


        file.close();

        float recvVel = (recvBytes-recvBytesOld)*8;
        float transVel = (transBytes-transBytesOld)*8;
        float recvTotal = recvBytes;
        float transTotal = transBytes;

        recvBytesOld = recvBytes;
        transBytesOld = transBytes;


        char recvTotalUnit = 0;
        char transTotalUnit = 0;
        char recvVelUnit = 0;
        char transVelUnit = 0;


        while (recvVel >= 1024) {
            recvVel /= 1024;
            ++recvVelUnit;
        }
        while (transVel >= 1024) {
            transVel /= 1024;
            ++transVelUnit;
        }
        while (recvTotal >= 1024) {
            recvTotal /= 1024;
            ++recvTotalUnit;
        }
        while (transTotal >= 1024) {
            transTotal /= 1024;
            ++transTotalUnit;
        }


        recvVel = std::floor(recvVel*100) / 100;
        transVel = std::floor(transVel*100) / 100;
        recvTotal = std::floor(recvTotal*100) / 100;
        transTotal = std::floor(transTotal*100) / 100;


        QString L11 = QString::number(recvVel);

        if (recvVelUnit == 0) L11.append(" b/s                   ");
        else if (recvVelUnit == 1) L11.append(" Kb/s                   ");
        else if (recvVelUnit == 2) L11.append(" Mb/s                   ");
        else if (recvVelUnit == 3) L11.append(" Gb/s                   ");

        QString L12 = QString::number(transVel);

        if (transVelUnit == 0) L12.append(" b/s    ");
        else if (transVelUnit == 1) L12.append(" Kb/s    ");
        else if (transVelUnit == 2) L12.append(" Mb/s    ");
        else if (transVelUnit == 3) L12.append(" Gb/s    ");



        QString L21 = QString::number(recvTotal);

        if (recvTotalUnit == 0) L21.append(" B                   ");
        else if (recvTotalUnit == 1) L21.append(" KB                   ");
        else if (recvTotalUnit == 2) L21.append(" MB                   ");
        else if (recvTotalUnit == 3) L21.append(" GB                   ");

        QString L22 = QString::number(transTotal);

        if (transTotalUnit == 0) L22.append(" B    ");
        else if (transTotalUnit == 1) L22.append(" KB    ");
        else if (transTotalUnit == 2) L22.append(" MB    ");
        else if (transTotalUnit == 3) L22.append(" GB    ");


        g15r_G15FPrint(canvas, (char *) "     RECEIVE       TRANSMIT", 0, 2, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 0);

        g15r_G15FPrint(canvas, (char *) L11.toStdString().c_str(), 0, 2, 1, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 2);
        g15r_G15FPrint(canvas, (char *) L12.toStdString().c_str(), 0, 2, 1, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 2);

        g15r_G15FPrint(canvas, (char *) L21.toStdString().c_str(), 0, 2, 1, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 3);
        g15r_G15FPrint(canvas, (char *) L22.toStdString().c_str(), 0, 2, 1, G15_JUSTIFY_RIGHT, G15_COLOR_BLACK, 3);



    }

    g15r_G15FPrint(canvas, (char *) "  ALL     CPU      MEM     NET", 0, 0, 1, G15_JUSTIFY_LEFT, G15_COLOR_BLACK, 5);
    g15_send(fd, (char *) canvas->buffer, G15_BUFFER_LEN);
}
