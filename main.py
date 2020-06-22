#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import signal
import datetime  # date --set "2020-06-21 21:45"
import serial    # sudo apt-get install -y python3-serial

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Gio
from gi.repository import GdkPixbuf

from itemTimbre import ItemTimbre

from globales import getHorarios
from globales import get_datetime_time_to_text
from globales import get_text_to_datetime_time

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

        '''self.set_default_size(640, 480)
        self.set_size_request(640, 480)'''

        self.__arduino = None

        self.set_icon_from_file(os.path.join(BASE_PATH, "logo.png"))
        self.set_resizable(True)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.headerBar = Gtk.HeaderBar()
        self.headerBar.set_show_close_button(True)
        self.headerBar.set_title("Timbre")
        self.set_titlebar(self.headerBar)

        boxbase = Gtk.VBox()
        scroll = Gtk.ScrolledWindow()
        scroll.get_style_context().add_class("scrolllist")
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(boxbase)
        self.add(scroll)

        grilla = Gtk.Grid()
        grilla.set_column_homogeneous(True)
        grilla.set_row_homogeneous(True)
        grilla.set_column_spacing(5)
        grilla.set_row_spacing(0)
        boxbase.pack_start(grilla, False, False, 0)

        self.__label = Gtk.Label("")
        self.__label.get_style_context().add_class("labelHora")        

        self.__timbresFrame = Gtk.Frame()
        self.__timbresFrame.get_style_context().add_class("frameTimbres")
        self.__timbresFrame.set_label(" Timbres: ")
        self.__timbresFrame.add(Gtk.VBox())

        scroll = Gtk.ScrolledWindow()
        scroll.get_style_context().add_class("scrolllist")
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.__timbresFrame)

        grilla.attach(scroll, 0, 0, 1, 22)
        grilla.attach(self.__label,1, 0, 1, 3)
        
        self.__error = Gtk.Label("ERROR")
        self.__error.get_style_context().add_class("alerta")
        grilla.attach(self.__error,1, 4, 1, 2)

        imagen = Gtk.Image.new_from_file(os.path.join(BASE_PATH, "logo.png"))
        grilla.attach(imagen, 1, 6, 1, 8)

        tocarTimbre = Gtk.Button("Tocar el Timbre")
        configurarTimbres = Gtk.Button("Configurar Timbres")
        configurarTimbres.set_sensitive(False)
        grilla.attach(configurarTimbres, 1, 16, 1, 2)
        grilla.attach(tocarTimbre, 1, 19, 1, 2)

        self.connect('realize', self.__realized)
        self.connect("delete-event", self.__salir)

        tocarTimbre.connect("clicked", self.__timbreSonar)
        configurarTimbres.connect("clicked", self.__config)

        self.__horarios = {}
        self.__timbre = None
        self.__duracion = 5
        self.__dia = 0

        try:
            self.__arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)
            #self.__arduino = serial.Serial('/dev/ttyACM1', 9600, timeout=0.1)
            self.__arduino.flushInput()
            self.__error.set_text("")
        except:
            self.__error.set_text("No se pudo establecer comunicacion usb")

        self.show_all()
        self.maximize()
        GLib.timeout_add(1000, self.__handle)
    
    def __config(self, widget):
        # FIXME: Falta implementar
        pass

    def __timbreSonar(self, widget):
        if widget:
            widget.set_sensitive(False)
            GLib.timeout_add(5000, widget.set_sensitive, True)

        try:
            self.__arduino.write(str.encode("%s" % self.__duracion))
            self.__arduino.flush()
            self.__error.set_text("")
        except:
            self.__error.set_text("No se pudo establecer comunicacion usb")
        
    def __handle(self):
        if not self.__arduino:
            try:
                self.__arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)
                #self.__arduino = serial.Serial('/dev/ttyACM1', 9600, timeout=0.1)
                self.__arduino.flushInput()
                self.__error.set_text("")
            except:
                self.__error.set_text("No se pudo establecer comunicacion usb")
        
        dt = datetime.datetime.now()
        tiempo = dt.time()
        self.__dia = dt.isoweekday()
        self.__label.set_text(get_datetime_time_to_text(tiempo))

        box = self.__timbresFrame.get_child()

        timbres = sorted(self.__horarios.keys())
        for timbre in timbres:
            index = timbres.index(timbre)

            if timbre < tiempo:
                box.get_children()[index].get_style_context().remove_class("timbreactual")
            else:
                box.get_children()[index-1].get_style_context().add_class("timbreactual")
                if self.__timbre != timbre:
                    self.__timbre = timbre
                    # FIXME: Cambiar esto por un entero. No se necesita una duración de mas de unos segundos.
                    self.__duracion = self.__horarios[timbre]['duracion'].second + \
                        (self.__horarios[timbre]['duracion'].minute * 60)
                    # FIXME: Solo sonará de Lunes a Viernes
                    if self.__dia < 6: self.__timbreSonar(None)
                break

        return True

    def __realized(self, widget):
        self.resize(640, 480)
        self.__timerLoad()
        
    def __salir(self, widget=None, senial=None):
        try:
            self.__arduino.close()
        except:
            pass
        sys.exit(0)

    def __timerLoad(self):
        box = self.__timbresFrame.get_child()
        for child in box.get_children():
            child.destroy()

        self.__horarios = getHorarios()
        timbres = sorted(self.__horarios.keys())
        
        for timbre in timbres:
            item = ItemTimbre(get_datetime_time_to_text(timbre))
            item.get_style_context().add_class("turno%s" % (int(self.__horarios[timbre]['turno'])%2))
            self.__timbresFrame.get_child().pack_start(item, False, False, 0)

        self.__timbresFrame.show_all()


if __name__ == "__main__":
    # FIXME: Verificar porque necesita ejecución como root
    GObject.threads_init()
    Gdk.threads_init()
    timbre = Timbre()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    exit_status = timbre.run(sys.argv)
    sys.exit(exit_status)
