#!/usr/local/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import python_wrapper as p
import numpy as np
import databaseWrapper as d

global MG;
MG = p.Model_Generator()

#Keep track of number of inputs the user enters
numInputs = 0;
def increment():
    global numInputs
    numInputs += 1

pName = "Transport, transit bus, diesel powered"
p1 = d.Process(pName)
spaLines = []

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
            #global p1
            #p1 = d.Process(pName)
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
        MG.run_spa("A03")
        #database = DatabaseResultsWindow()
        #database.window.show_all()
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


class RefineDialog:
    builder = Gtk.Builder()

    def __init__(self):
       RefineDialog.builder.add_from_file("refine_dialog.glade")
       RefineDialog.builder.connect_signals(self)
       self.window = RefineDialog.builder.get_object("window1")
       

    #TODO: functionality integration, all below is just a basic template
    def onYesClicked(self, button):
        print("yes clicked")
        #TODO: functionality integration
        #begin the database searching and open the database window
    def onNoClicked(self, button):
        self.window.destroy()
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

class DatabaseWindow:
    builder = Gtk.Builder()

    def __init__(self):
        DatabaseWindow.builder.add_from_file("database_window.glade")
        DatabaseWindow.builder.connect_signals(self)
        self.window = DatabaseWindow.builder.get_object("window1")
        
            

    #TODO: functionality integration, all below is just a basic template
    def onSearchClicked(self, button):
        #TODO: integrate the search with the actual model code, base window has text fields entry1 for NAICS and entry2 for a search term,
        #you can add more as needed
        return None

    #user clicks if they are done refining
    def onFinishClicked(self, button):
        #TODO: atm I set the window up thinking that the user clicks the search button to incrementally refine the model one component at a time, but this can be changed to have the user search a series of terms (i.e., enter info and then search, then the text entries clear)
        #and then click finish to update the model in a batch style when they are done adding components for the refinement, or something
        #whatever works best, up to you - NL
        self.window.destroy()

    def onDeleteWindow(self, *args):
	print("refine window closed")
        #Gtk.main_quit(*args)


class DatabaseResultsWindow:
    builder = Gtk.Builder()
    
    #constructor takes a list of tuples which are the names and amounts, this list is left empty if nothing is given
    def __init__(self, namesAndAmounts=[]):
        DatabaseResultsWindow.builder.add_from_file("databaseresults.glade")
        DatabaseResultsWindow.builder.connect_signals(self)
        self.window = DatabaseResultsWindow.builder.get_object("database_results")

        # Read SPA results and put lines in spaLines
        #with open("myfile4.txt","r") as f:
         #   global spaLines
          #  spaLines = f.readlines()
            
        #self.spaNumbers = spaResults(spaLines,0)  
        self.fruitList = ['apple', 'orange', 'banana', 'kiwi', 'strawberry']
        self.priceList = ['4.00', '3.00', '6.00', '5.00', '2.00']
        self.fruitsAndPrices = zip(self.fruitList, self.priceList)
        self.firstResultName = DatabaseResultsWindow.builder.get_object("firstResultName")
        self.firstResultAmount = DatabaseResultsWindow.builder.get_object("firstResultAmount")
        self.secondResultName = DatabaseResultsWindow.builder.get_object("secondResultName")
        self.secondResultAmount = DatabaseResultsWindow.builder.get_object("secondResultAmount")
        self.thirdResultName = DatabaseResultsWindow.builder.get_object("thirdResultName")
        self.thirdResultAmount = DatabaseResultsWindow.builder.get_object("thirdResultAmount")
        self.fourthResultName = DatabaseResultsWindow.builder.get_object("fourthResultName")
        self.fourthResultAmount = DatabaseResultsWindow.builder.get_object("fourthResultAmount")
        self.fifthResultName = DatabaseResultsWindow.builder.get_object("fifthResultName")
        self.fifthResultAmount = DatabaseResultsWindow.builder.get_object("fifthResultAmount")
        self.firstResultButton = DatabaseResultsWindow.builder.get_object("firstResultSelectButton")
        self.secondResultButton = DatabaseResultsWindow.builder.get_object("secondResultSelectButton")
        self.thirdResultButton = DatabaseResultsWindow.builder.get_object("thirdResultSelectButton")
        self.fourthResultButton = DatabaseResultsWindow.builder.get_object("fourthResultSelectButton")
        self.fifthResultButton = DatabaseResultsWindow.builder.get_object("fifthResultSelectButton")

        self.manualEntryName = DatabaseResultsWindow.builder.get_object("manualEntryName")
        self.manualEntryAmount = DatabaseResultsWindow.builder.get_object("manualEntryAmount")
        self.manualEntryButton = DatabaseResultsWindow.builder.get_object("manualEntrySelectButton")

        self.resultNames = [self.firstResultName, self.secondResultName, self.thirdResultName, self.fourthResultName, self.fifthResultName, self.manualEntryName]
        self.resultAmounts = [self.firstResultAmount, self.secondResultAmount, self.thirdResultAmount, self.fourthResultAmount, self.fifthResultAmount, self.manualEntryAmount]
        #self.window.show_all()

        
        if len(namesAndAmounts) == 0:
            namesAndAmounts = self.fruitsAndPrices #set the list to be this default if namesAndAmounts aren't given
            #a placeholder for now basically

            #reminder that default function args are set only once when the function is defined, so if you call the constructor multiple times
            #the list will change based on that
        for x in range(0, len(namesAndAmounts)):
            self.resultNames[x].set_text(namesAndAmounts[x][0])
            self.resultAmounts[x].set_text(namesAndAmounts[x][1])

        #set all of the results fields to be non-editable regardless of result presence
        for x in range(0, 5):
                self.resultNames[x].set_editable(False)
                self.resultAmounts[x].set_editable(False)

        self.buttonList = [self.firstResultButton, self.secondResultButton, self.thirdResultButton, self.fourthResultButton, self.fifthResultButton, self.manualEntryButton]

        #zip the results together into a three tuple list
        self.resultsContentAndButtons = zip(self.resultNames, self.resultAmounts, self.buttonList)

# reference for manual setting in case the above doesnt work for some reason - NL
        self.firstResultName.set_text(namesAndAmounts[0][0])
        self.firstResultAmount.set_text(namesAndAmounts[0][1])
        self.secondResultName.set_text(namesAndAmounts[1][0])
        self.secondResultAmount.set_text(namesAndAmounts[1][1])
        self.thirdResultName.set_text(namesAndAmounts[2][0])
        self.thirdResultAmount.set_text(namesAndAmounts[2][1])
        self.fourthResultName.set_text(namesAndAmounts[3][0])
        self.fourthResultAmount.set_text(namesAndAmounts[3][1])
        self.fifthResultName.set_text(namesAndAmounts[4][0])
        self.fifthResultAmount.set_text(namesAndAmounts[4][1])
        self.firstResultName.set_editable(False)
        self.firstResultAmount.set_editable(False)
        self.secondResultName.set_editable(False)
        self.secondResultAmount.set_editable(False)
        self.thirdResultName.set_editable(False)
        self.thirdResultAmount.set_editable(False)
        self.fourthResultName.set_editable(False)
        self.fourthResultAmount.set_editable(False)
        self.fifthResultName.set_editable(False)
        self.fifthResultAmount.set_editable(False)       
        
    
    def on_radiobutton1_toggled(self, button):
        print("toggle button 1 clicked")
        print(button.get_active())
            
    def on_radiobutton2_toggled(self, button):
        print("toggle button 2 clicked")
        
    def on_radiobutton3_toggled(self, button):
        print("toggle button 3 clicked")
        
    def on_radiobutton4_toggled(self, button):
        print("toggle button 4 clicked")
        
    def on_radiobutton5_toggled(self, button):
        print("toggle button 5 clicked")
        
    def on_radiobutton6_toggled(self, button):
        print("toggle button 6 clicked")
        
    def onDeleteWindow(self, *args):
        print("database results window closed")
	Gtk.main_quit(*args)

    def onManualEntryDataChanged(self, entry):
        #set the manual entry radio button to be active
        self.manualEntryButton.set_active(True)

    def onContinueClicked(self, button):
        print("continue button clicked")
        
        for x in range(0, 6):
            if (self.resultsContentAndButtons[x][2].get_active()):
                #get the text for this button's fields
                print("The following choice has been selected")
                print(self.resultsContentAndButtons[x][0].get_text() + ' ' + self.resultsContentAndButtons[x][1].get_text())
                break
            #destroy the window here and move on or something
    

window1 = ProcessOutputWindow()
Window2 = ProcessInputWindow()
econ = MatrixWindow()
#db_results = DatabaseResultsWindow()


Gtk.main()


# Returns the links from the line number (num) of the SPA results
def spaResults(lines, num):
    num = num+2
    allNumbers = []
    #model = lines[1].lstrip()
    for line in lines[num]:
        #value1 = line[:9]
        noValue1 = line[9:]
        f = len(noValue1) - len(noValue1.lstrip())
        noWhite = noValue1[f:]
        endNumbers = noWhite.find(" ")
        numbers = noWhite[:endNumbers].split("----")
        allNumbers.append(numbers)
        print(value1)
        print(numbers)
    return allNumbers
    
                
def getTop5(p1, num):
     naics = num #need function to get NAICS from SPA number
     results = p1.top5Inputs(naics)
     #print(results)
     return results

