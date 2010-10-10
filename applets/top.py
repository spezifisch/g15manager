import subprocess
import gobject

name = "Process Monitor"
description = "Shows the 4 processes\nthat consume more CPU"

def start():
    process = subprocess.Popen(["g15composer","/tmp/g15manager-top"])
    applet()
    gobject.timeout_add(2000, applet)
    return process

def applet():
    
    if not loop:
        return False

    stdout = subprocess.Popen(["top", "-b", "-n", "1"], stdout=subprocess.PIPE).stdout

    for i in range(7):
        stdout.readline()

    pid = ["","","",""]
    name = ["","","",""]
    cpu = ["","","",""]

    for i in range(4):
        process = stdout.readline().split()
        pid[i] = process[0]
        name[i] = process[11]
        cpu[i] = process[8]+"%"


    text = "MC 1\n" + \
        "TO 0  0 2 1 \"Process Monitor\"\n" + \
        "TO 0 10 1 0 \"%s\"\n" % pid[0] + \
        "TO 0 10 1 1 \"%s\"\n" % name[0] + \
        "TO 0 10 1 2 \"%s\"\n" % cpu[0] + \
        "TO 0 18 1 0 \"%s\"\n" % pid[1] + \
        "TO 0 18 1 1 \"%s\"\n" % name[1] + \
        "TO 0 18 1 2 \"%s\"\n" % cpu[1] + \
        "TO 0 26 1 0 \"%s\"\n" % pid[2] + \
        "TO 0 26 1 1 \"%s\"\n" % name[2] + \
        "TO 0 26 1 2 \"%s\"\n" % cpu[2] + \
        "TO 0 34 1 0 \"%s\"\n" % pid[3] + \
        "TO 0 34 1 1 \"%s\"\n" % name[3] + \
        "TO 0 34 1 2 \"%s\"\n" % cpu[3] + \
        "MC 0\n";


    with open("/tmp/g15manager-top", "w") as pipe:
        pipe.write(text)

    return loop