#!/usr/local/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk



class WindowOne:
    builder = Gtk.Builder()

    def __init__(self):
        WindowOne.builder.add_from_file("user_input_draft1.glade")
        WindowOne.builder.connect_signals(self)
        self.window = WindowOne.builder.get_object("window1")
        self.window.show_all()

    def onDeleteWindow(self, *args):
        print("window one closed")    

    def onButtonClicked(self, button):
        entry1 = WindowOne.builder.get_object("entry1")
        entry2 = WindowOne.builder.get_object("entry2")
        entry3 = WindowOne.builder.get_object("entry3")
        entry4 = WindowOne.builder.get_object("entry4")
        entry5 = WindowOne.builder.get_object("entry5")
        entry6 = WindowOne.builder.get_object("entry6")
        entry7 = WindowOne.builder.get_object("entry7")
        entry8 = WindowOne.builder.get_object("entry8")
        print(entry1.get_text())
        print(entry2.get_text())
        print(int(entry1.get_text(), 10) + int(entry2.get_text(), 10))
        self.window.destroy()
        econ.window.show_all()
        print("window two opened")
class WindowTwo:
    builder = Gtk.Builder()

    def __init__(self):
        WindowTwo.builder.add_from_file("user_input_draft2.glade")
        WindowTwo.builder.connect_signals(self)
        self.window = WindowTwo.builder.get_object("econ_window")
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)    

    def onButtonClicked(self, button):
        entry1 = WindowTwo.builder.get_object("entry1")
        entry2 = WindowTwo.builder.get_object("entry2")
        entry3 = WindowTwo.builder.get_object("entry3")
        entry4 = WindowTwo.builder.get_object("entry4")
        print(entry1.get_text())
        print(entry2.get_text())
        print(entry3.get_text())
        print(entry4.get_text())
        self.window.destroy()
        ##window.destroy()
        #WindowTwo.builder.add_from_file("user_input_draft2.glade")
        #WindowTwo.builder.connect_signals(Handler())
        #newWindow = WindowTwo.builder.get_object("econ_window")
        #newWindow.show_all()

#def handleTransition(*args):
    #create a WindowTwo object
	


#window 1 object
window1 = WindowOne()
econ = WindowTwo()
#builder = Gtk.Builder()
#builder.add_from_file("user_input_draft1.glade")
#builder.connect_signals(Handler())

#window = builder.get_object("window1")
#window.show_all()

Gtk.main()
