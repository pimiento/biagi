#!/usr/bin/env python3
import sys, os
import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, GObject, Gtk

class GTK_Main(object):

    def __init__(self):
        window = Gtk.Window(title="MP3-Player")
        window.set_default_size(400, 200)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, True, 0)
        self.entry1 = Gtk.Entry()
        vbox.pack_start(self.entry1, False, True, 0)
        self.button = Gtk.Button(label="Start")
        self.button.connect("clicked", self.start_stop)
        vbox.add(self.button)
        window.show_all()

        self.player = Gst.Pipeline.new("player")
        source = Gst.ElementFactory.make("filesrc", "file-source")
        decoder = Gst.ElementFactory.make("mpg123audiodec", "mp3-decoder")
        conv = Gst.ElementFactory.make("audioconvert", "converter")
        sink = Gst.ElementFactory.make("alsasink", "alsa-output")

        self.player.add(source)
        self.player.add(decoder)
        self.player.add(conv)
        self.player.add(sink)
        source.link(decoder)
        decoder.link(conv)
        conv.link(sink)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        self.player1 = Gst.Pipeline.new("player1")
        source1 = Gst.ElementFactory.make("filesrc", "file-source")
        decoder1 = Gst.ElementFactory.make("mpg123audiodec", "mp3-decoder")
        conv1 = Gst.ElementFactory.make("audioconvert", "converter")
        sink1 = Gst.ElementFactory.make("alsasink", "alsa-output")

        self.player1.add(source1)
        self.player1.add(decoder1)
        self.player1.add(conv1)
        self.player1.add(sink1)
        source1.link(decoder1)
        decoder1.link(conv1)
        conv1.link(sink1)

        bus1 = self.player.get_bus()
        bus1.add_signal_watch()
        bus1.connect("message", self.on_message)

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            filepath = self.entry.get_text().strip()
            filepath1 = self.entry1.get_text().strip()
            if os.path.isfile(filepath):
                filepath = os.path.realpath(filepath)
                filepath1 = os.path.realpath(filepath1)
                self.button.set_label("Stop")
                self.player.get_by_name("file-source").set_property("location", filepath)
                self.player.set_state(Gst.State.PLAYING)
                self.player1.get_by_name("file-source").set_property("location", filepath1)
                self.player1.set_state(Gst.State.PLAYING)
            else:
                self.player.set_state(Gst.State.NULL)
                self.player1.set_state(Gst.State.NULL)
                self.button.set_label("Start")

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)

Gst.init(None)
GTK_Main()
# GObject.threads_init()
Gtk.main()
