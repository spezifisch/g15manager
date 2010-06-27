import gtk
import applets.amarok
import applets.top
import subprocess

class Main:
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("gui.glade")
        builder.connect_signals(self)

        self.check_amarok = builder.get_object("check_amarok")
        self.check_top = builder.get_object("check_top")
        self.check_g15stats = builder.get_object("check_g15stats")
        self.g15stats_interface = builder.get_object("g15stats_interface")

        self.processes = [0,0,0]

    def check_g15stats_toggled(self,widget):
        if self.check_g15stats.get_active() == True: 
            self.processes[0] = subprocess.Popen(["g15stats","-i",self.g15stats_interface.get_text()])
        else:
            self.processes[0].kill()


    def check_amarok_toggled(self,widget):        
        if self.check_amarok.get_active() == True:
            applets.amarok.loop = True
            self.processes[1] = applets.amarok.start(self.check_amarok)
        else:
            applets.amarok.loop = False
            self.processes[1].kill()


    def check_top_toggled(self,widget):
        if self.check_top.get_active() == True:
            applets.top.loop = True
            self.processes[2] = applets.top.start()
        else:
            applets.top.loop = False
            self.processes[2].kill()


if __name__ == "__main__":
    Main = Main()
    gtk.main()
