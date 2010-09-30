# coding: UTF-8

import ctypes
import subprocess
import socket


import applets
import keys
import glib
import gtk
import gobject
import gettext
import gconf


class Main:
    def __init__(self):
        builder = gtk.Builder()
        builder.set_translation_domain("g15manager")
        builder.add_from_file("g15manager.ui")
        builder.connect_signals(self)

        self.window = builder.get_object("window")
        self.gmail_save = builder.get_object("gmail_save")
        self.gmail_user = builder.get_object("gmail_user")
        self.gmail_passwd = builder.get_object("gmail_passwd")
        self.gmail_update_interval = builder.get_object("gmail_update_interval")
        self.network_interface = builder.get_object("network_interface")
        self.popup_menu = builder.get_object("popup_menu")
        self.iconview = builder.get_object("iconview")
        self.notebook = builder.get_object("notebook")
        self.applets = builder.get_object("applets")
        self.treeview = builder.get_object("treeview")
        self.info_label = builder.get_object("info_label")
        self.use_gk = builder.get_object("use_gk")
        self.toggle_bindings = builder.get_object("toggle_bindings")
        self.start_minimized = builder.get_object("start_minimized")
        self.item_show_hide = builder.get_object("item_show_hide")    
        self.keys_m1 = builder.get_object("keys_m1")
        self.keys_m2 = builder.get_object("keys_m2")
        self.keys_m3 = builder.get_object("keys_m3")
        self.keys_treeview = builder.get_object("keys_treeview")
        self.rb_m1 = builder.get_object("rb_m1")
        self.rb_m2 = builder.get_object("rb_m2")
        self.rb_m3 = builder.get_object("rb_m3")
        self.keys_renderer2 = builder.get_object("keys_renderer2")
        self.keys_renderer3 = builder.get_object("keys_renderer3")


	gettext.textdomain("g15manager")
	gettext.bindtextdomain("g15manager")
	self._ = gettext.gettext


        self.statusicon = gtk.StatusIcon()
        self.statusicon.set_from_file("icons/g15.png")
        self.statusicon.connect("popup-menu", self.statusicon_right_click)
        self.statusicon.connect("activate", self.show_hide)
        self.statusicon.set_visible(True)

        #self.iconview.set_cursor(0, cell=None, start_editing=False)

        self.processes = [0, 0, 0, 0, 0, 0, 0, 0]


        self.config = gconf.client_get_default()

        if self.config.get_string("/apps/g15manager/network_interface"):
            self.network_interface.set_text(self.config.get_string("/apps/g15manager/network_interface"))

        if 0 < self.config.get_int("/apps/g15manager/gmail/update_interval"):
            self.gmail_update_interval.set_value(self.config.get_int("/apps/g15manager/gmail/update_interval"))
        else:
            self.gmail_update_interval.set_value(1)


        self.use_gk.set_active(self.config.get_bool("/apps/g15manager/gmail/gnomekeyring"))
        self.start_minimized.set_active(self.config.get_bool("/apps/g15manager/start_minimized"))
        self.toggle_bindings.set_active(self.config.get_bool("/apps/g15manager/bindings"))

        self.applets.set_value(self.applets.get_iter(0), 1, self.config.get_bool("/apps/g15manager/startup/amarok"))
        self.applets.set_value(self.applets.get_iter(1), 1, self.config.get_bool("/apps/g15manager/startup/audacious"))
        self.applets.set_value(self.applets.get_iter(2), 1, self.config.get_bool("/apps/g15manager/startup/emesene"))
        self.applets.set_value(self.applets.get_iter(3), 1, self.config.get_bool("/apps/g15manager/startup/exaile"))
        self.applets.set_value(self.applets.get_iter(4), 1, self.config.get_bool("/apps/g15manager/startup/g15stats"))
        self.applets.set_value(self.applets.get_iter(5), 1, self.config.get_bool("/apps/g15manager/startup/gmail"))
        self.applets.set_value(self.applets.get_iter(6), 1, self.config.get_bool("/apps/g15manager/startup/rhythmbox"))
        self.applets.set_value(self.applets.get_iter(7), 1, self.config.get_bool("/apps/g15manager/startup/process_monitor"))



        self.keys_m1.set_value(self.keys_m1.get_iter(0), 1, self.config.get_string("/apps/g15manager/commands/M1/G1"))
        self.keys_m1.set_value(self.keys_m1.get_iter(1), 1, self.config.get_string("/apps/g15manager/commands/M1/G2"))
        self.keys_m1.set_value(self.keys_m1.get_iter(2), 1, self.config.get_string("/apps/g15manager/commands/M1/G3"))
        self.keys_m1.set_value(self.keys_m1.get_iter(3), 1, self.config.get_string("/apps/g15manager/commands/M1/G4"))
        self.keys_m1.set_value(self.keys_m1.get_iter(4), 1, self.config.get_string("/apps/g15manager/commands/M1/G5"))
        self.keys_m1.set_value(self.keys_m1.get_iter(5), 1, self.config.get_string("/apps/g15manager/commands/M1/G6"))

        self.keys_m2.set_value(self.keys_m2.get_iter(0), 1, self.config.get_string("/apps/g15manager/commands/M2/G1"))
        self.keys_m2.set_value(self.keys_m2.get_iter(1), 1, self.config.get_string("/apps/g15manager/commands/M2/G2"))
        self.keys_m2.set_value(self.keys_m2.get_iter(2), 1, self.config.get_string("/apps/g15manager/commands/M2/G3"))
        self.keys_m2.set_value(self.keys_m2.get_iter(3), 1, self.config.get_string("/apps/g15manager/commands/M2/G4"))
        self.keys_m2.set_value(self.keys_m2.get_iter(4), 1, self.config.get_string("/apps/g15manager/commands/M2/G5"))
        self.keys_m2.set_value(self.keys_m2.get_iter(5), 1, self.config.get_string("/apps/g15manager/commands/M2/G6"))

        self.keys_m3.set_value(self.keys_m3.get_iter(0), 1, self.config.get_string("/apps/g15manager/commands/M3/G1"))
        self.keys_m3.set_value(self.keys_m3.get_iter(1), 1, self.config.get_string("/apps/g15manager/commands/M3/G2"))
        self.keys_m3.set_value(self.keys_m3.get_iter(2), 1, self.config.get_string("/apps/g15manager/commands/M3/G3"))
        self.keys_m3.set_value(self.keys_m3.get_iter(3), 1, self.config.get_string("/apps/g15manager/commands/M3/G4"))
        self.keys_m3.set_value(self.keys_m3.get_iter(4), 1, self.config.get_string("/apps/g15manager/commands/M3/G5"))
        self.keys_m3.set_value(self.keys_m3.get_iter(5), 1, self.config.get_string("/apps/g15manager/commands/M3/G6"))




        for i in range(8):
            iter = self.applets.get_iter(i)
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                self.toggle_applet(None, i)



        if not self.start_minimized.get_active():
            self.window.show()
            self.item_show_hide.set_label(self._("Hide"))
            self.window_is_visible = True
        else:
            self.window_is_visible = False


        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("localhost", 15550))
        if self.socket.recv(16) != "G15 daemon HELLO":
            raise Exception("Communication error with server")
        self.socket.setblocking(0)

        self.rb_m1.set_active(True)

        gobject.timeout_add(50, keys.catch_keys, self.socket, self.toggle_bindings,
                self.keys_m1, self.keys_m2, self.keys_m3,
                self.rb_m1.get_active(), self.rb_m2.get_active(), self.rb_m3.get_active())


    def show_hide(self, widget):
        if self.window_is_visible:
            self.window.hide()
            self.item_show_hide.set_label(self._("Show"))
            self.window_is_visible = False
        else:
            self.window.present()
            self.item_show_hide.set_label(self._("Hide"))
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


    def memory_changed(self, widget):
        if self.rb_m1.get_active():
            self.keys_treeview.set_model(self.keys_m1)

        elif self.rb_m2.get_active():
            self.keys_treeview.set_model(self.keys_m2)

        elif self.rb_m3.get_active():
            self.keys_treeview.set_model(self.keys_m3)



    def keys_command_edited(self, widget, item, text):
        if self.rb_m1.get_active():
            iter = self.keys_m1.get_iter(int(item))
            self.keys_m1.set_value(iter, 1, text)
            self.config.set_string("/apps/g15manager/commands/M1/G%i" % (int(item)+1), self.keys_m1.get_value(iter, 1))

        elif self.rb_m2.get_active():
            iter = self.keys_m2.get_iter(int(item))
            self.keys_m2.set_value(iter, 1, text)
            self.config.set_string("/apps/g15manager/commands/M2/G%i" % (int(item)+1), self.keys_m2.get_value(iter, 1))

        elif self.rb_m3.get_active():
            iter = self.keys_m3.get_iter(int(item))
            self.keys_m3.set_value(iter, 1, text)
            self.config.set_string("/apps/g15manager/commands/M3/G%i" % (int(item)+1), self.keys_m3.get_value(iter, 1))



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

            self.config.set_bool("/apps/g15manager/startup/amarok", self.applets.get_value(iter, 1))

        elif item == 1:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                applets.audacious.loop = False
                self.processes[1].kill()
            else:
                self.applets.set_value(iter, 1, True)
                applets.audacious.loop = True
                self.processes[1] = applets.audacious.start()

            self.config.set_bool("/apps/g15manager/startup/audacious", self.applets.get_value(iter, 1))

        elif item == 2:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                applets.emesene.loop = False
                self.processes[2].kill()
            else:
                self.applets.set_value(iter, 1, True)
                applets.emesene.loop = True
                self.processes[2] = applets.emesene.start()

            self.config.set_bool("/apps/g15manager/startup/emesene", self.applets.get_value(iter, 1))

        elif item == 3:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                applets.exaile.loop = False
                self.processes[3].kill()
            else:
                self.applets.set_value(iter, 1, True)
                applets.exaile.loop = True
                self.processes[3] = applets.exaile.start()

            self.config.set_bool("/apps/g15manager/startup/exaile", self.applets.get_value(iter, 1))

        elif item == 4:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                self.processes[4].kill()
            else:
                self.applets.set_value(iter, 1, True)
                self.processes[4] = subprocess.Popen(["g15stats", "-i", self.network_interface.get_text()])

            self.config.set_bool("/apps/g15manager/startup/g15stats", self.applets.get_value(iter, 1))
            self.config.set_string("/apps/g15manager/network_interface", self.network_interface.get_text())

        elif item == 5:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                applets.gmail.loop = False
                self.processes[5].kill()
            else:
                self.applets.set_value(iter, 1, True)
                applets.gmail.loop = True
                self.processes[5] = applets.gmail.start(self.gmail_user.get_text(), self.gmail_passwd.get_text(), self.gmail_update_interval.get_value_as_int())

            self.config.set_bool("/apps/g15manager/startup/gmail", self.applets.get_value(iter, 1))

        elif item == 6:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                applets.rhythmbox.loop = False
                self.processes[6].kill()
            else:
                self.applets.set_value(iter, 1, True)
                applets.rhythmbox.loop = True
                self.processes[6] = applets.rhythmbox.start()

            self.config.set_bool("/apps/g15manager/startup/rhythmbox", self.applets.get_value(iter, 1))

        elif item == 7:
            if self.applets.get_value(iter, 1):
                self.applets.set_value(iter, 1, False)
                applets.top.loop = False
                self.processes[7].kill()
            else:
                self.applets.set_value(iter, 1, True)
                applets.top.loop = True
                self.processes[7] = applets.top.start()

            self.config.set_bool("/apps/g15manager/startup/process_monitor", self.applets.get_value(iter, 1))



    def save_gmail(self, widget):
        if self.use_gk.get_active():
            applets.gmail.save(self.gmail_user.get_text(), self.gmail_passwd.get_text())


    def gmail_update_interval_value_changed(self, widget):
        self.config.set_int("/apps/g15manager/gmail/update_interval", self.gmail_update_interval.get_value_as_int())


    def show_aboutdialog(self, widget):
        dialog = gtk.AboutDialog()
        dialog.set_name("G15 Manager")
        dialog.set_version("0.3")
        dialog.set_authors(["Nofre Móra"])
        dialog.set_website("https://launchpad.net/g15manager")
        dialog.run()
        dialog.destroy()

    def use_gk_toggled(self, widget):
        if self.use_gk.get_active():
            self.gmail_save.show()

            user, passwd = applets.gmail.load()
            self.gmail_user.set_text(user)
            self.gmail_passwd.set_text(passwd)

        else:
            self.gmail_save.hide()

        self.config.set_bool("/apps/g15manager/gmail/gnomekeyring", self.use_gk.get_active())


    def toggle_bindings_toggled(self, widget):
        self.config.set_bool("/apps/g15manager/bindings", self.toggle_bindings.get_active())


    def start_minimized_toggled(self, widget):
        self.config.set_bool("/apps/g15manager/start_minimized", self.start_minimized.get_active())


    def applet_info(self, widget):
        item = self.treeview.get_cursor()[0][0]
        if item == 0:
            self.info_label.set_text(self._("Shows the Amarok's\ncurrent track"))
        elif item == 1:
            self.info_label.set_text(self._("Shows the Audacious's\ncurrent track"))
        elif item == 2:
            self.info_label.set_text(self._("Shows the number of unread\nmessages of Emesene"))
        elif item == 3:
            self.info_label.set_text(self._("Shows the Exaile's\ncurrent track"))
        elif item == 4:
            self.info_label.set_text(self._("Shows the use of CPU, memory,\nswap and network, temperatures\nand more"))
        elif item == 5:
            self.info_label.set_text(self._("Shows the unread mails\nof your Gmail account"))
        elif item == 6:
            self.info_label.set_text(self._("Shows the Rhythmbox's\ncurrent track"))
        elif item == 7:
            self.info_label.set_text(self._("Shows the 4 processes\nthat consume more CPU"))


if __name__ == "__main__":
    glib.set_application_name("G15 Manager")
    
    libc = ctypes.cdll.LoadLibrary("libc.so.6")
    buff = ctypes.create_string_buffer(11)
    buff.value = "g15manager"
    libc.prctl(15, ctypes.byref(buff), 0, 0, 0)

    Main = Main()
    gtk.main()