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
import gettext
import keybinder

class Main:
    def __init__(self):
        builder = gtk.Builder()
        builder.set_translation_domain("g15manager")
        builder.add_from_file("g15manager.ui")
        builder.connect_signals(self)

        self.window = builder.get_object("window")
        self.gmail_user = builder.get_object("gmail_user")
        self.gmail_passwd = builder.get_object("gmail_passwd")
        self.gmail_update_interval = builder.get_object("gmail_update_interval")
        self.g15stats_interface = builder.get_object("g15stats_interface")     
        self.popup_menu = builder.get_object("popup_menu")
        self.iconview = builder.get_object("iconview")
        self.notebook = builder.get_object("notebook")
        self.applets = builder.get_object("applets")
        self.treeview = builder.get_object("treeview")
        self.info_label = builder.get_object("info_label")
        self.use_gk = builder.get_object("use_gk")
        self.enable_bindings = builder.get_object("enable_bindings")
        self.start_minimized = builder.get_object("start_minimized")
        self.item_show_hide = builder.get_object("item_show_hide")    
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


	gettext.textdomain("g15manager")
	gettext.bindtextdomain("g15manager")
	_ = gettext.gettext

#        import appindicator
#        indicator = appindicator.Indicator("g15manager",
#                "distributor-logo", appindicator.CATEGORY_APPLICATION_STATUS)
#        indicator.set_status (appindicator.STATUS_ACTIVE)
#        indicator.set_menu(self.popup_menu)

        self.statusicon = gtk.StatusIcon()
        self.statusicon.set_from_file("icons/g15.png")
        self.statusicon.connect("popup-menu", self.statusicon_right_click)
        self.statusicon.connect("activate", self.show_hide)
        self.statusicon.set_visible(True)

        #self.iconview.set_cursor(0, cell=None, start_editing=False)

        self.processes = [0, 0, 0, 0, 0, 0, 0]

        self.gmail_update_interval.set_value(1)

        self.config = ConfigParser.ConfigParser()
        try:
            self.config.read("%s/.g15manager" % os.environ["HOME"])

            self.g15stats_interface.set_text(self.config.get("g15manager", "g15stats_interface"))
            self.gmail_update_interval.set_value(self.config.getint("g15manager", "gmail_update_interval"))
            self.use_gk.set_active(self.config.getboolean("g15manager", "use_gk"))
            self.start_minimized.set_active(self.config.getboolean("g15manager", "start_minimized"))

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
            self.config.set("g15manager", "start_minimized", False)
            self.config.set("g15manager", "gmail_update_interval", 1)
            with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
                self.config.write(configfile)

        self.load_gmail()

        for i in range(7):
            iter = self.applets.get_iter(i)
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                self.toggle_applet(None, i)


        self.keys = [["G1",self.command_g1], ["G2",self.command_g2], ["G3",self.command_g3],
                    ["G4",self.command_g4], ["G5",self.command_g5], ["G6",self.command_g6],
                    ["G7",self.command_g7], ["G8",self.command_g8], ["G9",self.command_g9],
                    ["G10",self.command_g10], ["G11",self.command_g11], ["G12",self.command_g12],
                    ["G13",self.command_g13], ["G14",self.command_g14], ["G15",self.command_g15],
                    ["G16",self.command_g16], ["G17",self.command_g17], ["G18",self.command_g18]]


        if not self.start_minimized.get_active():
            self.window.show()
            self.item_show_hide.set_label("Hide")
            self.window_is_visible = True
        else:
            self.window_is_visible = False


    def show_hide(self, widget):
        if self.window_is_visible:
            self.window.hide()
            self.item_show_hide.set_label("Show")
            self.window_is_visible = False
        else:
            self.window.present()
            self.item_show_hide.set_label("Hide")
            self.window_is_visible = True


    def statusicon_right_click(self, icon, button, time):
        self.popup_menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.statusicon)


    def quit(self, widget):
        for i in self.processes:
            if i != 0:
                i.kill()
        gtk.main_quit()


    def window_hide(self, widget, data=None):
        self.show_hide(widget)
        return True


    def enable_bindings_toggled(self, widget):
        if self.enable_bindings.get_active():
            for key in self.keys:
                keybinder.bind(key[0], self.key_pressed, key[0])
        else:
            for key in self.keys:
                keybinder.unbind(key[0])


    def key_pressed(self, pressed_key):
        if self.enable_bindings.get_active():
            for key in self.keys:
                if pressed_key == key[0]:
                    command = key[1].get_text().split(" ")
                    command_list = []
                    for arg in command:
                        command_list.append(arg)
                    subprocess.Popen(command_list)


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
                self.processes[5] = applets.gmail.start(self.gmail_user.get_text(), self.gmail_passwd.get_text(), self.gmail_update_interval.get_value_as_int())

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

        self.config.set("g15manager", "gmail_update_interval", self.gmail_update_interval.get_value_as_int())
        with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
            self.config.write(configfile)

        print self.gmail_update_interval.get_value_as_int()


    def load_gmail(self):
        if self.use_gk.get_active():
            user, passwd = applets.gmail.load()
            self.gmail_user.set_text(user)
            self.gmail_passwd.set_text(passwd)


    def show_aboutdialog(self, widget):
        dialog = gtk.AboutDialog()
        dialog.set_name("G15 Manager")
        dialog.set_version("0.2")
        dialog.set_authors(["Nofre Móra"])
        dialog.set_website("https://launchpad.net/g15manager")
        dialog.run()
        dialog.destroy()

    def use_gk_toggled(self, widget):
        self.config.set("g15manager", "use_gk", self.use_gk.get_active())
        with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
            self.config.write(configfile)
        self.load_gmail()


    def start_minimized_toggled(self, widget):
        self.config.set("g15manager", "start_minimized", self.start_minimized.get_active())
        with open("%s/.g15manager" % os.environ["HOME"], "w") as configfile:
            self.config.write(configfile)


    def applet_info(self, widget):
        item = self.treeview.get_cursor()[0][0]
        if item == 0:
            self.info_label.set_text(_("Shows the Amarok's\n current track"))
        elif item == 1:
            self.info_label.set_text(_("Shows the Audacious's\n current track"))
        elif item == 2:
            self.info_label.set_text(_("Shows the number of unread\nmessages of Emesene"))
        elif item == 3:
            self.info_label.set_text(_("Shows the Exaile's\n current track"))
        elif item == 4:
            self.info_label.set_text(_("Shows the use of CPU, memory,\nswap and network, temperatures\nand more"))
        elif item == 5:
            self.info_label.set_text(_("Shows the unread mails\nof your Gmail account"))
        elif item == 6:
            self.info_label.set_text(_("Shows the 4 processes\n that consume more CPU"))

if __name__ == "__main__":
    glib.set_application_name("G15 Manager")
    
    libc = ctypes.cdll.LoadLibrary("libc.so.6")
    buff = ctypes.create_string_buffer(11)
    buff.value = "g15manager"
    libc.prctl(15, ctypes.byref(buff), 0, 0, 0)

    Main = Main()
    gtk.main()