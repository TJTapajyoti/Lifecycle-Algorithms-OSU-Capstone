#!/usr/local/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import python_wrapper as p

global MG;
MG = p.Model_Generator()

#Keep track of number of inputs the user enters
numInputs = 0;
def increment():
    global numInputs
    numInputs += 1

pName = "Transport, transit bus, diesel powered"

class ProcessOutputWindow:
    builder = Gtk.Builder()
    
    def __init__(self):
        ProcessOutputWindow.builder.add_from_file("user_input_draft1.glade")
        ProcessOutputWindow.builder.connect_signals(self)
        self.window = ProcessOutputWindow.builder.get_object("window1")
        self.window.show_all()

    def onDeleteWindow(self, *args):
        print("window one closed")    

    def onButtonClicked(self, button):
        entry1 = ProcessOutputWindow.builder.get_object("entry1")
        entry2 = ProcessOutputWindow.builder.get_object("entry2")
        entry3 = ProcessOutputWindow.builder.get_object("entry3")
        entry4 = ProcessOutputWindow.builder.get_object("entry4")
        entry5 = ProcessOutputWindow.builder.get_object("entry5")
        errorMessage = ProcessOutputWindow.builder.get_object("label1")
        try:
            global pName
            pName = entry1.get_text()
            code = entry2.get_text()
            amt = int(entry3.get_text())
            price = float(entry4.get_text())
            MG.add_process_output(code,amt,price)
            ei = float(entry5.get_text())
            MG.add_environmental_impact(ei)
            self.window.destroy()
            print("window one closed")
            Window2.window.show_all()
            print("window two opened")
        except:
            errorMessage.set_label("Invalid Input")
            entry1.set_text("")
            entry2.set_text("")
            entry3.set_text("")
            entry4.set_text("")
            entry5.set_text("")
       
class ProcessInputWindow:
    builder = Gtk.Builder()
    
    def __init__(self):
        ProcessInputWindow.builder.add_from_file("process_inputs.glade")
        ProcessInputWindow.builder.connect_signals(self)
        self.window = ProcessInputWindow.builder.get_object("window1")
        title = ProcessInputWindow.builder.get_object("label4")
        title.set_label("Input1")
        increment()
        
    def onDeleteWindow(self, *args):
        self.window.destroy()
        print("window two closed")    

    def onButton1Clicked(self, button1):
        entry1 = ProcessInputWindow.builder.get_object("entry1")
        entry2 = ProcessInputWindow.builder.get_object("entry2")
        entry3 = ProcessInputWindow.builder.get_object("entry3")
        errorMessage = ProcessInputWindow.builder.get_object("label5")
        if entry1.get_text() == "" and entry2.get_text() == "" and entry3.get_text() == "":
            self.window.destroy()
            print("Window two closed")
            econ.window.show_all()
            print("window three opened")
        else:
            try:
                code = entry1.get_text()
                amt = float(entry2.get_text())
                price = float(entry3.get_text())
                MG.add_process_input(code,amt,price)
                print("Input"+str(numInputs))
                print("NAICS: "+entry1.get_text())
                print("AMT: "+entry2.get_text())
                print("Price: "+entry3.get_text())
                self.window.destroy()
                print("Window two closed")
                econ.window.show_all()
                print("window three opened")
            except:
                errorMessage.set_label("Invalid Input")
                entry1.set_text("")
                entry2.set_text("")
                entry3.set_text("")
        
            
    def onButton2Clicked(self, button2):
        entry1 = ProcessInputWindow.builder.get_object("entry1")
        entry2 = ProcessInputWindow.builder.get_object("entry2")
        entry3 = ProcessInputWindow.builder.get_object("entry3")
        errorMessage = ProcessInputWindow.builder.get_object("label5")
        try:
            code = entry1.get_text()
            amt = float(entry2.get_text())
            price = float(entry3.get_text())
            MG.add_process_input(code,amt,price)
            print("Input "+str(numInputs))
            print("NAICS: "+entry1.get_text())
            print("AMT: "+entry2.get_text())
            print("Price: "+entry3.get_text())
            errorMessage.set_text("")
            increment()
        except:
            errorMessage.set_text("Invalid Input")
        entry1.set_text("")
        entry2.set_text("")
        entry3.set_text("")
        title = ProcessInputWindow.builder.get_object("label4")
        title.set_label("Input"+str(numInputs))

        
class MatrixWindow:
    builder = Gtk.Builder()

    def __init__(self):
        MatrixWindow.builder.add_from_file("user_input_draft2.glade")
        MatrixWindow.builder.connect_signals(self)
        self.window = MatrixWindow.builder.get_object("econ_window")
        
    def onDeleteWindow(self, *args):
        print("window three closed")     

    def onButtonClicked(self, button):
        entry1 = MatrixWindow.builder.get_object("entry1")
        entry2 = MatrixWindow.builder.get_object("entry2")
        entry3 = MatrixWindow.builder.get_object("entry3")
        entry4 = MatrixWindow.builder.get_object("entry4")
        v = entry1.get_text()
        u = entry2.get_text()
        b = entry3.get_text()
        codes = entry4.get_text()
        print("U: "+v)
        print("V: "+u)
        print("B: "+b)
        print("Codes: "+codes)
        MG.add_v(v)
        MG.add_u(u)
        MG.add_b(b)
        MG.add_codes(codes)
        self.window.destroy()
        print("window three closed")
        print("window four opened")
        MG.run_spa("A03") #Need to change from hard code
        spa = SpaWindow()
        spa.window.show_all()
        
    #file dialog event handlers so user can browse/upload instead of entering file path manually
    def on_file_button1_clicked(self, button):
        print("clicked file chooser button")
        fileDialog = Gtk.FileChooserDialog("Select a File", None, Gtk.FileChooserAction.OPEN, ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))

        response = fileDialog.run()

        entry1 = MatrixWindow.builder.get_object("entry1")
        if response == Gtk.ResponseType.OK:
            print("You clicked the Open button")
            print("File selected " + fileDialog.get_filename())
            entry1.set_text(fileDialog.get_filename())

        

        elif response == Gtk.ResponseType.CANCEL:
            print("User did not select a file")

        fileDialog.destroy()

    def on_file_button2_clicked(self, button):
        print("clicked file chooser button")
        fileDialog = Gtk.FileChooserDialog("Select a File", None, Gtk.FileChooserAction.OPEN, ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))

        response = fileDialog.run()

        entry2 = MatrixWindow.builder.get_object("entry2")
        if response == Gtk.ResponseType.OK:
            print("You clicked the Open button")
            print("File selected " + fileDialog.get_filename())
            entry2.set_text(fileDialog.get_filename())

        elif response == Gtk.ResponseType.CANCEL:
            print("User did not select a file")

        fileDialog.destroy()

    def on_file_button3_clicked(self, button):
        print("clicked file chooser button")
        fileDialog = Gtk.FileChooserDialog("Select a File", None, Gtk.FileChooserAction.OPEN, ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))

        response = fileDialog.run()

        entry3 = MatrixWindow.builder.get_object("entry3")
        if response == Gtk.ResponseType.OK:
            print("You clicked the Open button")
            print("File selected " + fileDialog.get_filename())
            entry3.set_text(fileDialog.get_filename())

        elif response == Gtk.ResponseType.CANCEL:
            print("User did not select a file")

        fileDialog.destroy()


    def on_file_button4_clicked(self, button):
        print("clicked file chooser button")
        fileDialog = Gtk.FileChooserDialog("Select a File", None, Gtk.FileChooserAction.OPEN, ("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK))

        response = fileDialog.run()

        entry4 = MatrixWindow.builder.get_object("entry4")
        if response == Gtk.ResponseType.OK:
            print("You clicked the Open button")
            print("File selected " + fileDialog.get_filename())
            entry4.set_text(fileDialog.get_filename())

        elif response == Gtk.ResponseType.CANCEL:
            print("User did not select a file")

        fileDialog.destroy()


class SpaWindow:
    builder = Gtk.Builder()

    def __init__(self):
        SpaWindow.builder.add_from_file("SPA_results.glade")
        SpaWindow.builder.connect_signals(self)
        self.window = SpaWindow.builder.get_object("window1")
        title = SpaWindow.builder.get_object("label2")
        myfile4 = open("myfile4.txt","r")
        results = myfile4.read()
        title.set_label(results)
        
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)


window1 = ProcessOutputWindow()
Window2 = ProcessInputWindow()
econ = MatrixWindow()

Gtk.main()



