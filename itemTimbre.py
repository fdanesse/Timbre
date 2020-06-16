#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class ItemTimbre(Gtk.HBox):

    def __init__(self, timbre):

        Gtk.HBox.__init__(self)

        self.__timbre = timbre
        self.__label = Gtk.Label(self.__timbre)
        self.__progress = Gtk.ProgressBar()

        self.pack_start(self.__label, False, False, 0)
        self.pack_start(self.__progress, False, False, 0)

        self.show_all()

    def setTimbre(timbre):
        self.__timbre = timbre

    def getTimbre():
        return self.__timbre
        