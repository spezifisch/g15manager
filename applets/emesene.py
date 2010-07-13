# coding: UTF-8

import subprocess
import dbus
import gobject

def start():

    states = {"NLN":"Online", "HDN":"Hidden",
        "AWY": "Away", "BSY": "Busy",
        "BRB": "Right Back", "PHN": "On the Phone",
        "LUN": "Go to Lunch", "IDL": "Idle"}

    process = subprocess.Popen(["g15composer", "/tmp/g15manager-emesene"])

    gobject.timeout_add(1000, applet, states)

    return process

def applet(states):
    if not loop:
        return False

    try:
        bus = dbus.SessionBus()
        emesenebus = bus.get_object("org.emesene.dbus", "/org/emesene/dbus")

        user = str(emesenebus.get_user_account())
        status = states[emesenebus.get_status()]
        count = int(emesenebus.get_message_count())

        if count == 0:
            line4 = "TO 1 36 1 0 \"There aren't new messages\"\n"
        elif count == 1:
            line4 = "TO 1 36 1 0 \"There is a new message\"\n"
        else:
            line4 = "TO 1 36 1 0 \"There are %i new messages\"\n" % count

        text = "MC 1\n" + "TO 0  0 2 1 \"Emesene\"\n" + \
            "TO 1 14 1 0 \"User: %s\"\n" % user + \
            "TO 1 26 1 0 \"Status: %s\"\n" % status + line4 + "MC 0\n";


    except:
        text = "MC 1\n" + "TO 0 14 1 1 \"Emesene isn't running\"\n" + \
            "TO 0 22 1 1 \"or the D-Bus plugin is disabled\"\n"  "MC 0\n"


    with open("/tmp/g15manager-emesene", "w") as pipe:
        pipe.write(text)

    return loop