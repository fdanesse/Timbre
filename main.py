#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import signal
import time
import datetime

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Gio

from itemTimbre import ItemTimbre

from globales import getHorarios
from globales import get_time_to_text
from globales import get_text_to_time

BASE_PATH = os.path.dirname(__file__)

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(BASE_PATH, "Estilos", "estilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()
context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_SETTINGS)


class Timbre(Gtk.Application):

    def __init__(self):

        Gtk.Application.__init__(self)
        
        self.set_flags(Gio.ApplicationFlags.NON_UNIQUE | Gio.ApplicationFlags.HANDLES_OPEN)

    def do_activate(self, files=[]):
        self.win = TimbreWindow(self, files)
        self.win.show()

    '''def do_open(self, files, i, hint):
        # [__gi__.GLocalFile]  https://docs.python.org/3/library/filesys.html
        self.do_activate(files)'''

    #def do_startup (self):
    #    Gtk.Application.do_startup(self)


class TimbreWindow(Gtk.ApplicationWindow):

    def __init__(self, app, files=[]):

        Gtk.Window.__init__(self, title="Timbre", application=app)

        self.set_default_size(640, 480)
        self.set_size_request(640, 480)

        #self.set_icon_from_file(os.path.join(BASE_PATH, "Iconos", "JAMedia.svg"))
        self.set_resizable(True)
        self.set_position(Gtk.WindowPosition.CENTER)

        #self.headerBar = HeaderBar()
        #self.headerBar.set_title(title)
        #self.set_titlebar(self.headerBar)

        boxbase = Gtk.VBox()
        self.add(boxbase)

        self.__label = Gtk.Label("")
        boxbase.pack_start(self.__label, False, False, 0)

        self.__timbresFrame = Gtk.Frame()
        self.__timbresFrame.set_label(" Timbres: ")
        self.__timbresFrame.add(Gtk.VBox())

        boxbase.pack_start(self.__timbresFrame, False, False, 0)

        self.connect('realize', self.__realized)
        self.connect("delete-event", self.__salir)

        self.__horarios = {}

        self.show_all()

        GLib.timeout_add(1000, self.__handle)
    
    def __handle(self):
        tiempo = time.gmtime()
        self.__label.set_text(get_time_to_text(tiempo))
        return True

    def __realized(self, widget):     
        self.resize(640, 480)
        self.__timerLoad()
        
    def __salir(self, widget=None, senial=None):
        #Gtk.main_quit()
        sys.exit(0)

    def __timerLoad(self):
        box = self.__timbresFrame.get_child()
        for child in box.get_children():
            child.destroy()

        #tiempo = time.gmtime()
        self.__horarios = getHorarios()
        timbres = sorted(self.__horarios.keys())
        
        for t in timbres:
            item = ItemTimbre(get_time_to_text(t))
            self.__timbresFrame.get_child().pack_start(item, False, False, 0)
        self.__timbresFrame.show_all()


if __name__ == "__main__":
    GObject.threads_init()
    Gdk.threads_init()
    timbre = Timbre()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit_status = timbre.run(sys.argv)
    sys.exit(exit_status)
    #Gtk.main()
