# coding: UTF-8

import ConfigParser
import ctypes
import os
import subprocess

import applets.amarok
import applets.audacious
import applets.emesene
import applets.exaile
import applets.gmail
import applets.top
import glib
import gtk
import keybinder

class Main:
    def __init__(self):
        builder = gtk.Builder()
        builder.set_translation_domain("g15manager")
        builder.add_from_file("g15manager.ui")
        builder.connect_signals(self)


        self.window = builder.get_object("window")
        self.check_amarok = builder.get_object("check_amarok")
        self.check_top = builder.get_object("check_top")
        self.check_emesene = builder.get_object("check_emesene")
        self.check_g15stats = builder.get_object("check_g15stats")
        self.check_gmail = builder.get_object("check_gmail")
        self.gmail_user = builder.get_object("gmail_user")
        self.gmail_passwd = builder.get_object("gmail_passwd")
        self.g15stats_interface = builder.get_object("g15stats_interface")     
        self.popup_menu = builder.get_object("popup_menu")
        self.iconview = builder.get_object("iconview")
        self.notebook = builder.get_object("notebook")
        self.applets = builder.get_object("applets")
        self.treeview = builder.get_object("treeview")
        self.use_gk = builder.get_object("use_gk")

        self.command_g1 = builder.get_object("command_g1")
        self.command_g2 = builder.get_object("command_g2")
        self.command_g3 = builder.get_object("command_g3")
        self.command_g4 = builder.get_object("command_g4")
        self.command_g5 = builder.get_object("command_g5")
        self.command_g6 = builder.get_object("command_g6")
        self.command_g7 = builder.get_object("command_g7")
        self.command_g8 = builder.get_object("command_g8")
        self.command_g9 = builder.get_object("command_g9")
        self.command_g10 = builder.get_object("command_g10")
        self.command_g11 = builder.get_object("command_g11")
        self.command_g12 = builder.get_object("command_g12")
        self.command_g13 = builder.get_object("command_g13")
        self.command_g14 = builder.get_object("command_g14")
        self.command_g15 = builder.get_object("command_g15")
        self.command_g16 = builder.get_object("command_g16")
        self.command_g17 = builder.get_object("command_g17")
        self.command_g18 = builder.get_object("command_g18")

#        import appindicator
#        indicator = appindicator.Indicator("g15manager",
#                "distributor-logo", appindicator.CATEGORY_APPLICATION_STATUS)
#        indicator.set_status (appindicator.STATUS_ACTIVE)
#        indicator.set_menu(self.popup_menu)

        self.statusicon = gtk.StatusIcon()
        self.statusicon.set_from_file("icons/g15.png")
        self.statusicon.connect("popup-menu", self.statusicon_right_click)
        self.statusicon.connect("activate", self.statusicon_left_click)
        self.statusicon.set_visible(True)

        #self.iconview.set_cursor(0, cell=None, start_editing=False)

        self.processes = [0, 0, 0, 0, 0, 0, 0]


        self.config = ConfigParser.ConfigParser()
        try:
            self.config.read("%s/.g15manager" % os.environ["HOME"])

            self.g15stats_interface.set_text(self.config.get("g15manager", "g15stats_interface"))
            self.use_gk.set_active(self.config.getboolean("g15manager", "use_gk"))

            self.applets.set_value(self.applets.get_iter(0), 1, self.config.getboolean("g15manager", "launch_amarok"))
            self.applets.set_value(self.applets.get_iter(1), 1, self.config.getboolean("g15manager", "launch_audacious"))
            self.applets.set_value(self.applets.get_iter(2), 1, self.config.getboolean("g15manager", "launch_emesene"))
            self.applets.set_value(self.applets.get_iter(3), 1, self.config.getboolean("g15manager", "launch_exaile"))
            self.applets.set_value(self.applets.get_iter(4), 1, self.config.getboolean("g15manager", "launch_g15stats"))
            self.applets.set_value(self.applets.get_iter(5), 1, self.config.getboolean("g15manager", "launch_gmail"))
            self.applets.set_value(self.applets.get_iter(6), 1, self.config.getboolean("g15manager", "launch_top"))

        except:
            with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
                configfile.write("[g15manager]")
            self.config.read("%s/.g15manager" % os.environ["HOME"])
            self.config.set("g15manager", "launch_g15stats", False)
            self.config.set("g15manager", "g15stats_interface", "")
            self.config.set("g15manager", "launch_amarok", False)
            self.config.set("g15manager", "launch_top", False)
            self.config.set("g15manager", "launch_emesene", False)
            self.config.set("g15manager", "launch_gmail", False)
            self.config.set("g15manager", "launch_exaile", False)
            self.config.set("g15manager", "launch_audacious", False)
            self.config.set("g15manager", "use_gk", False)
            with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
                self.config.write(configfile)

        self.load_gmail()

        for i in range(7):
            iter = self.applets.get_iter(i)
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                self.toggle_applet(None, i)


        keys = ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12", "G13", "G14", "G15", "G16", "G17", "G18"]


        for key in keys:
            keybinder.bind(key, self.key_pressed, key)


    def statusicon_left_click(self, widget):
        if self.window.is_active() == True:
            self.window.hide()
        else:
            self.window.present()

    def statusicon_right_click(self, icon, button, time):
        self.popup_menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.statusicon)


    def quit(self, widget):
        for i in self.processes:
            if i != 0:
                i.kill()
        gtk.main_quit()


    def window_hide(self, widget, data=None):
        self.window.hide()
        return True

    def key_pressed(self, key):
        if key == "G1":
            subprocess.Popen(self.command_g1.get_text())
        elif key == "G2":
            subprocess.Popen(self.command_g2.get_text())
        elif key == "G3":
            subprocess.Popen(self.command_g3.get_text())
        elif key == "G4":
            subprocess.Popen(self.command_g4.get_text())
        elif key == "G5":
            subprocess.Popen(self.command_g5.get_text())
        elif key == "G6":
            subprocess.Popen(self.command_g6.get_text())
        elif key == "G7":
            subprocess.Popen(self.command_g7.get_text())
        elif key == "G8":
            subprocess.Popen(self.command_g8.get_text())
        elif key == "G9":
            subprocess.Popen(self.command_g9.get_text())
        elif key == "G10":
            subprocess.Popen(self.command_g10.get_text())
        elif key == "G11":
            subprocess.Popen(self.command_g11.get_text())
        elif key == "G12":
            subprocess.Popen(self.command_g12.get_text())
        elif key == "G13":
            subprocess.Popen(self.command_g13.get_text())
        elif key == "G14":
            subprocess.Popen(self.command_g14.get_text())
        elif key == "G15":
            subprocess.Popen(self.command_g15.get_text())
        elif key == "G16":
            subprocess.Popen(self.command_g16.get_text())
        elif key == "G17":
            subprocess.Popen(self.command_g17.get_text())
        elif key == "G18":
            subprocess.Popen(self.command_g18.get_text())


    def change_page(self, widget):
        self.notebook.set_current_page(self.iconview.get_selected_items()[0][0])

    def toggle_applet(self, widget, item):
        item = int(item)
        iter = self.applets.get_iter(item)

        if item == 0:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                applets.amarok.loop = False
                self.processes[0].kill()
            else:
                self.applets.set_value(iter, 1, True)
                applets.amarok.loop = True
                self.processes[0] = applets.amarok.start()

            self.config.set("g15manager", "launch_amarok", self.applets.get_value(iter, 1))

        elif item == 1:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                applets.audacious.loop = False
                self.processes[1].kill()
            else:
                self.applets.set_value(iter, 1, True)
                applets.audacious.loop = True
                self.processes[1] = applets.audacious.start()

            self.config.set("g15manager", "launch_audacious", self.applets.get_value(iter, 1))

        elif item == 2:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                applets.emesene.loop = False
                self.processes[2].kill()
            else:
                self.applets.set_value(iter, 1, True)
                applets.emesene.loop = True
                self.processes[2] = applets.emesene.start()

            self.config.set("g15manager", "launch_emesene", self.applets.get_value(iter, 1))

        elif item == 3:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                applets.exaile.loop = False
                self.processes[3].kill()
            else:
                self.applets.set_value(iter, 1, True)
                applets.exaile.loop = True
                self.processes[3] = applets.exaile.start()

            self.config.set("g15manager", "launch_exaile", self.applets.get_value(iter, 1))

        elif item == 4:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                self.processes[4].kill()
            else:
                self.applets.set_value(iter, 1, True)
                self.processes[4] = subprocess.Popen(["g15stats", "-i", self.g15stats_interface.get_text()])

            self.config.set("g15manager", "launch_g15stats", self.applets.get_value(iter, 1))
            self.config.set("g15manager", "g15stats_interface", self.g15stats_interface.get_text())

        elif item == 5:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                applets.gmail.loop = False
                self.processes[5].kill()
            else:
                self.applets.set_value(iter, 1, True)
                applets.gmail.loop = True
                self.processes[5] = applets.gmail.start(self.gmail_user.get_text(), self.gmail_passwd.get_text(), 1)

            self.config.set("g15manager", "launch_gmail", self.applets.get_value(iter, 1))

        elif item == 6:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                applets.top.loop = False
                self.processes[6].kill()
            else:
                self.applets.set_value(iter, 1, True)
                applets.top.loop = True
                self.processes[6] = applets.top.start()

            self.config.set("g15manager", "launch_top", self.applets.get_value(iter, 1))


        with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
            self.config.write(configfile)

    def save_gmail(self, widget):
        if self.use_gk.get_active():
            applets.gmail.save(self.gmail_user.get_text(), self.gmail_passwd.get_text())

    def load_gmail(self):
        if self.use_gk.get_active():
            user, passwd = applets.gmail.load()
            self.gmail_user.set_text(user)
            self.gmail_passwd.set_text(passwd)

    def show_aboutdialog(self, widget):
        dialog = gtk.AboutDialog()
        dialog.set_name("G15 Daemon")
        dialog.set_version("0.1.x")
        dialog.set_authors(["Nofre Móra"])
        dialog.set_website("https://launchpad.net/g15manager")
        dialog.run()
        dialog.destroy()

    def use_gk_toggled(self, widget):
        self.config.set("g15manager", "use_gk", self.use_gk.get_active())
        with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
            self.config.write(configfile)
        self.load_gmail()


if __name__ == "__main__":
    glib.set_application_name("G15 Manager")
    
    libc = ctypes.cdll.LoadLibrary("libc.so.6")
    buff = ctypes.create_string_buffer(11)
    buff.value = "g15manager"
    libc.prctl(15, ctypes.byref(buff), 0, 0, 0)

    Main = Main()
    gtk.main()