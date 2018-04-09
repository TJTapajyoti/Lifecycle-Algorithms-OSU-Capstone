#!/usr/local/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import databaseWrapper as d
import csv
    
limit1 = 0
limit2 = 0
line = 0

# get the NAICS code from sectorsCodes csv file
def getCode(num):
    naics = 0
    with open('SectorsCodes.csv','rb') as f:
        sectorCodes = csv.reader(f)
        for row in sectorCodes:
            if row[0] == num:
                naics = row[1]
    return naics
    
# Get the links for each line of the the SPA results
spaLinks = []
with open("myfile4.txt","r") as f:
    spaLines = f.readlines()
    for line in spaLines[2:]:
        noValue1 = line[9:]
        x = len(noValue1) - len(noValue1.lstrip())
        noWhite = noValue1[x:]
        #print(noWhite)
        endNumbers = noWhite.find(" ")
        numbers = noWhite[:endNumbers].split("----")
        print(numbers)
        spaLinks.append(numbers)
    f.close()

class limitsWindow:
    builder = Gtk.Builder()

    def __init__(self):
       limitsWindow.builder.add_from_file("refine_dialog.glade")
       limitsWindow.builder.connect_signals(self)
       self.window = limitsWindow.builder.get_object("window1")
       self.window.show_all()
       
    #TODO: functionality integration, all below is just a basic template
    def onContinue(self, button):
        global limit1
        limit1 = limitsWindow.builder.get_object("entry1").get_text()
        global limit2
        limit2 = limitsWindow.builder.get_object("entry2").get_text()
        self.window.destroy()
        process.window.show_all()
        
    def onDeleteWindow(self, *args):
	self.window.destroy()
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
	self.window.destroy()
        Gtk.main_quit(*args)


class ProcessWindow:
    builder = Gtk.Builder()
    
    #constructor takes the row number from the spa results and index of the link in the row 
    def __init__(self, row, i):
        ProcessWindow.builder.add_from_file("databaseresults.glade")
        ProcessWindow.builder.connect_signals(self)
        self.window = ProcessWindow.builder.get_object("database_results")
        self.title = ProcessWindow.builder.get_object("label1")
        
        # name labels
        self.firstResultName = ProcessWindow.builder.get_object("firstResultName")
        self.secondResultName = ProcessWindow.builder.get_object("secondResultName")
        self.thirdResultName = ProcessWindow.builder.get_object("thirdResultName")
        self.fourthResultName = ProcessWindow.builder.get_object("fourthResultName")
        self.fifthResultName = ProcessWindow.builder.get_object("fifthResultName")
        # name text field
        self.manualEntryName = ProcessWindow.builder.get_object("manualEntryName")
        
        # radio buttons
        self.firstResultButton = ProcessWindow.builder.get_object("firstResultSelectButton")
        self.secondResultButton = ProcessWindow.builder.get_object("secondResultSelectButton")
        self.thirdResultButton = ProcessWindow.builder.get_object("thirdResultSelectButton")
        self.fourthResultButton = ProcessWindow.builder.get_object("fourthResultSelectButton")
        self.fifthResultButton = ProcessWindow.builder.get_object("fifthResultSelectButton")
        self.manualEntryButton = ProcessWindow.builder.get_object("manualEntrySelectButton")

        # set title and get top 5 results
        link = spaLinks[row][i]
        naics = getCode(link)
        self.title.set_text("Process Name for NAICS: " + str(naics))
        description = d.NAICSdescription(naics)
        results = d.top5Processes(description)
        
        # populate name fields with top 5 results for first line
        try:
            self.firstResultName.set_text(results[0])
        except:
            self.firstResultName.set_text("...")
        try:
            self.secondResultName.set_text(results[1])
        except:
            self.secondResultName.set_text("...")
        try:
            self.thirdResultName.set_text(results[2])
        except:
            self.thirdResultName.set_text("...")
        try:
            self.fouthResultName.set_text(results[3])
        except:
            self.fourthResultName.set_text("...")
        try:
            self.fifthResultName.set_text(results[4])
        except:
            self.fifthResultName.set_text("...")

            
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
        self.window.destroy()
	Gtk.main_quit(*args)
        
    def onManualEntryDataChanged(self, entry):
        #set the manual entry radio button to be active
        self.manualEntryButton.set_active(True)
        
    def onContinueClicked(self, button):
        # if there are inputs to the process, open up the top 5 inputs window. Else if there are more processes in the link, open up a new process window. Else perform calculations
        self.window.destroy()
        
class DatabaseResultsWindow:
    builder = Gtk.Builder()
    
    #constructor takes a list of tuples which are the names and amounts, this list is left empty if nothing is given
    def __init__(self, namesAndAmounts=[]):
        DatabaseResultsWindow.builder.add_from_file("databaseresults.glade")
        DatabaseResultsWindow.builder.connect_signals(self)
        self.window = DatabaseResultsWindow.builder.get_object("database_results")
        self.title = DatabaseResultsWindow.builder.get_object("label1")

        # name and amount labels
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
        # name and amount text fields
        self.manualEntryName = DatabaseResultsWindow.builder.get_object("manualEntryName")
        self.manualEntryAmount = DatabaseResultsWindow.builder.get_object("manualEntryAmount")
        
        # radio buttons
        self.firstResultButton = DatabaseResultsWindow.builder.get_object("firstResultSelectButton")
        self.secondResultButton = DatabaseResultsWindow.builder.get_object("secondResultSelectButton")
        self.thirdResultButton = DatabaseResultsWindow.builder.get_object("thirdResultSelectButton")
        self.fourthResultButton = DatabaseResultsWindow.builder.get_object("fourthResultSelectButton")
        self.fifthResultButton = DatabaseResultsWindow.builder.get_object("fifthResultSelectButton")
        self.manualEntryButton = DatabaseResultsWindow.builder.get_object("manualEntrySelectButton")

        self.resultNames = [self.firstResultName, self.secondResultName, self.thirdResultName, self.fourthResultName, self.fifthResultName, self.manualEntryName]
        self.resultAmounts = [self.firstResultAmount, self.secondResultAmount, self.thirdResultAmount, self.fourthResultAmount, self.fifthResultAmount, self.manualEntryAmount]

        
        #if len(namesAndAmounts) == 0:
            #namesAndAmounts = self.fruitsAndPrices #set the list to be this default if namesAndAmounts aren't given
            #a placeholder for now basically

            #reminder that default function args are set only once when the function is defined, so if you call the constructor multiple times
            #the list will change based on that
   
        
        '''
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
'''
        
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
        self.window.destroy()
	Gtk.main_quit(*args)

    def onManualEntryDataChanged(self, entry):
        #set the manual entry radio button to be active
        self.manualEntryButton.set_active(True)
'''
    def onContinueClicked(self, button):
        print("continue button clicked")
        
        for x in range(0, 6):
            if (self.resultsContentAndButtons[x][2].get_active()):
                #get the text for this button's fields
                print("The following choice has been selected")
                print(self.resultsContentAndButtons[x][0].get_text() + ' ' + self.resultsContentAndButtons[x][1].get_text())
                break
            #destroy the window here and move on or something
'''

# Main
limits = limitsWindow()
process = ProcessWindow(0,0)

Gtk.main()



