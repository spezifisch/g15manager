import subprocess
import ConfigParser
import applets.amarok
import applets.emesene
import applets.top
import applets.gmail
import gtk
import keybinder
import os


class Main:
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("gui.glade")
        builder.connect_signals(self)

        import gkeys

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
        self.statusicon.set_from_file("g15.png")
        self.statusicon.connect("popup-menu", self.statusicon_right_click)
        self.statusicon.connect("activate", self.statusicon_left_click)
        self.statusicon.set_visible(True)


        self.processes = [0, 0, 0, 0, 0]

        self.config = ConfigParser.ConfigParser()
        try:
            self.config.read("%s/.g15manager" % os.environ["HOME"])
            self.check_g15stats.set_active(self.config.getboolean("g15manager","launch_g15stats"))
            self.g15stats_interface.set_text(self.config.get("g15manager","g15stats_interface"))
            self.check_amarok.set_active(self.config.getboolean("g15manager","launch_amarok"))
            self.check_top.set_active(self.config.getboolean("g15manager","launch_top"))
            self.check_emesene.set_active(self.config.getboolean("g15manager","launch_emesene"))
            self.check_gmail.set_active(self.config.getboolean("g15manager","launch_gmail"))

        except:
            with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
                configfile.write("[g15manager]")
            self.config.read("%s/.g15manager" % os.environ["HOME"])
            self.config.set("g15manager","launch_g15stats",self.check_g15stats.get_active())
            self.config.set("g15manager","g15stats_interface",self.g15stats_interface.get_text())
            self.config.set("g15manager","launch_amarok",self.check_amarok.get_active())
            self.config.set("g15manager","launch_top",self.check_top.get_active())
            self.config.set("g15manager","launch_emesene",self.check_emesene.get_active())
            self.config.set("g15manager","launch_gmail",self.check_gmail.get_active())
            with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
                self.config.write(configfile)


        keys = ["G1","G2","G3","G4","G5","G6","G7","G8","G9","G10","G11","G12","G13","G14","G15","G16","G17","G18"]


        for key in keys:
            keybinder.bind(key, self.key_pressed, key)


    def statusicon_left_click(self, widget):
        if self.window.is_active() == True:
            self.window.hide()
        else:
            self.window.present()

    def statusicon_right_click(self,icon,button,time):
        self.popup_menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.statusicon)


    def quit(self, widget):
        for i in self.processes:
            if i != 0:
                i.kill()
        gtk.main_quit()


    def window_hide(self,widget,data=None):
        self.window.hide()
        return True


    def check_g15stats_toggled(self, widget):
        if self.check_g15stats.get_active() == True: 
            self.processes[0] = subprocess.Popen(["g15stats", "-i", self.g15stats_interface.get_text()])
        else:
            self.processes[0].kill()

        self.config.set("g15manager","launch_g15stats",self.check_g15stats.get_active())
        self.config.set("g15manager","g15stats_interface",self.g15stats_interface.get_text())
        with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
                self.config.write(configfile)


    def check_amarok_toggled(self, widget):
        if self.check_amarok.get_active() == True:
            applets.amarok.loop = True
            self.processes[1] = applets.amarok.start(self.check_amarok)
        else:
            applets.amarok.loop = False
            if self.processes[1] != 0:
                self.processes[1].kill()

        self.config.set("g15manager","launch_amarok",self.check_amarok.get_active())
        with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
                self.config.write(configfile)

    def check_top_toggled(self, widget):
        if self.check_top.get_active() == True:
            applets.top.loop = True
            self.processes[2] = applets.top.start()
        else:
            applets.top.loop = False
            self.processes[2].kill()

        self.config.set("g15manager","launch_top",self.check_top.get_active())
        with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
                self.config.write(configfile)

    def check_emesene_toggled(self, widget):
        if self.check_emesene.get_active() == True:
            applets.emesene.loop = True
            self.processes[3] = applets.emesene.start(self.check_emesene)
        else:
            applets.emesene.loop = False
            if self.processes[3] != 0:
                self.processes[3].kill()

        self.config.set("g15manager","launch_emesene",self.check_emesene.get_active())
        with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
                self.config.write(configfile)

    def check_gmail_toggled(self, widget):
        if self.check_gmail.get_active() == True:
            applets.gmail.loop = True
            self.processes[4] = applets.gmail.start(self.gmail_user.get_text(),self.gmail_passwd.get_text(),1)
        else:
            applets.gmail.loop = False
            if self.processes[4] != 0:
                self.processes[4].kill()

        self.config.set("g15manager","launch_gmail",self.check_gmail.get_active())
        with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
                self.config.write(configfile)

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


if __name__ == "__main__":
    Main = Main()
    gtk.main()