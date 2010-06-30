import subprocess
import ConfigParser
import applets.amarok
import applets.emesene
import applets.top
import gtk
import os

class Main:
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("gui.glade")
        builder.connect_signals(self)

        self.check_amarok = builder.get_object("check_amarok")
        self.check_top = builder.get_object("check_top")
        self.check_emesene = builder.get_object("check_emesene")
        self.check_g15stats = builder.get_object("check_g15stats")
        self.check_gmail = builder.get_object("check_gmail")
        self.g15stats_interface = builder.get_object("g15stats_interface")

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
            self.save_config()

        self.processes = [0, 0, 0, 0]
        


    def window_destroy(self,widget):
        for i in self.processes:
            if i != 0:
                i.kill()
        gtk.main_quit()

    def save_config(self):
        self.config.set("g15manager","launch_g15stats",self.check_g15stats.get_active())
        self.config.set("g15manager","g15stats_interface",self.g15stats_interface.get_text())
        self.config.set("g15manager","launch_amarok",self.check_amarok.get_active())
        self.config.set("g15manager","launch_top",self.check_top.get_active())
        self.config.set("g15manager","launch_emesene",self.check_emesene.get_active())
        self.config.set("g15manager","launch_gmail",self.check_gmail.get_active())
        with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
                self.config.write(configfile)



    def check_g15stats_toggled(self, widget):
        if self.check_g15stats.get_active() == True: 
            self.processes[0] = subprocess.Popen(["g15stats", "-i", self.g15stats_interface.get_text()])
        else:
            self.processes[0].kill()

        self.save_config()


    def check_amarok_toggled(self, widget):
        if self.check_amarok.get_active() == True:
            applets.amarok.loop = True
            self.processes[1] = applets.amarok.start(self.check_amarok)
        else:
            applets.amarok.loop = False
            if self.processes[1] != 0:
                self.processes[1].kill()

        self.save_config()

    def check_top_toggled(self, widget):
        if self.check_top.get_active() == True:
            applets.top.loop = True
            self.processes[2] = applets.top.start()
        else:
            applets.top.loop = False
            self.processes[2].kill()

        self.save_config()

    def check_emesene_toggled(self, widget):
        if self.check_emesene.get_active() == True:
            applets.emesene.loop = True
            self.processes[3] = applets.emesene.start(self.check_emesene)
        else:
            applets.emesene.loop = False
            if self.processes[3] != 0:
                self.processes[3].kill()

        self.save_config()


if __name__ == "__main__":
    Main = Main()
    gtk.main()
