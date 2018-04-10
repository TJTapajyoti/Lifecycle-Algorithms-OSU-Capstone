#!/usr/local/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import databaseWrapper as d
import csv
import sys
    
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

# get the industry description from sectorsCodes csv file
def getDescr(num):
    descr = ""
    with open('SectorsCodes.csv','rb') as f:
        sectorCodes = csv.reader(f)
        for row in sectorCodes:
            if row[0] == num:
                descr = row[2]
    return descr

# Get the links for each line of the the SPA results
def getSPAlinks():
    spaLinks = []
    with open("myfile4.txt","r") as f:
        spaLines = f.readlines()
        for line in spaLines[2:]:
            noValue1 = line[9:]
            x = len(noValue1) - len(noValue1.lstrip())
            noWhite = noValue1[x:]
            endNumbers = noWhite.find(" ")
            numbers = noWhite[:endNumbers].split("----")
            spaLinks.append(numbers)
        f.close()
    return spaLinks


class limitsWindow:

    def __init__(self):
       self.builder = Gtk.Builder()
       self.builder.add_from_file("refine_dialog.glade")
       self.builder.connect_signals(self)
       self.window = self.builder.get_object("window1")
       self.window.show_all()
       
    #TODO: functionality integration, all below is just a basic template
    def onContinue(self, button):
        global limit1
        limit1 = self.builder.get_object("entry1").get_text()
        global limit2
        limit2 = self.builder.get_object("entry2").get_text()
        self.window.destroy()
        Gtk.main_quit()

    def onDeleteWindow(self, *args):
	self.window.destroy()
        Gtk.main_quit(*args)
        sys.exit()
      

class ProcessWindow:

    
    #constructor takes the row number from the spa results and index of the link in the row 
    def __init__(self, link):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("processWindow.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("database_results")
        self.title = self.builder.get_object("label1")
        
        # name labels
        self.firstResultName = self.builder.get_object("firstResultName")
        self.secondResultName = self.builder.get_object("secondResultName")
        self.thirdResultName = self.builder.get_object("thirdResultName")
        self.fourthResultName = self.builder.get_object("fourthResultName")
        self.fifthResultName = self.builder.get_object("fifthResultName")
        # name text field
        self.manualEntryName = self.builder.get_object("manualEntryName")
        
        # radio buttons
        self.firstResultButton = self.builder.get_object("firstResultSelectButton")
        self.secondResultButton = self.builder.get_object("secondResultSelectButton")
        self.thirdResultButton = self.builder.get_object("thirdResultSelectButton")
        self.fourthResultButton = self.builder.get_object("fourthResultSelectButton")
        self.fifthResultButton = self.builder.get_object("fifthResultSelectButton")
        self.manualEntryButton = self.builder.get_object("manualEntrySelectButton")

        # set title and get top 5 results
        naics = getCode(link)
        self.title.set_text("Process Name for NAICS: " + str(naics))
        description = [getDescr(link)]
        print(description)
        self.results = d.top5Processes(description)
        print(self.results)
        if len(self.results) < 5:
            description = d.NAICSdescription(naics)
            self.results = self.results + d.top5Processes(description)
        self.toggle = 6    

        # populate name fields with top 5 results for first line
        try:
            self.firstResultName.set_text(str(self.results[0]))
        except:
            self.firstResultName.set_text("...")
        try:
            self.secondResultName.set_text(str(self.results[1]))
        except:
            self.secondResultName.set_text("...")
        try:
            self.thirdResultName.set_text(str(self.results[2]))
        except:
            self.thirdResultName.set_text("...")
        try:
            self.fourthResultName.set_text(str(self.results[3]))
        except:
            self.fourthResultName.set_text("...")
        try:
            self.fifthResultName.set_text(str(self.results[4]))
        except:
            self.fifthResultName.set_text("...")

    def on_radiobutton1_toggled(self, button):
        self.toggle = 1
            
    def on_radiobutton2_toggled(self, button):
        self.toggle = 2
        
    def on_radiobutton3_toggled(self, button):
        self.toggle = 3
        
    def on_radiobutton4_toggled(self, button):
        self.toggle = 4
        
    def on_radiobutton5_toggled(self, button):
        self.toggle = 5
        
    def on_radiobutton6_toggled(self, button):
        self.toggle = 6
        
    def onDeleteWindow(self, *args):
        self.window.destroy()
	Gtk.main_quit(*args)
        sys.exit()
        print("delete-event signal happened for ProcessWindow class")
        
    def onManualEntryDataChanged(self, entry):
        #set the manual entry radio button to be active
        self.manualEntryButton.set_active(True)
        
    def onContinueClicked(self, button):
        if self.toggle == 1:
            self.results = self.results[0]
        elif self.toggle == 2:
            self.results = self.results[1]
        elif self.toggle == 3:
            self.results = self.results[2]
        elif self.toggle == 4:
            self.results = self.results[3]
        elif self.toggle == 5:
            self.results = self.results[4]
        elif self.toggle == 6:
            self.results = self.manualEntryName.get_text()
        print(self.results)
        self.window.destroy()
        Gtk.main_quit()
        '''
        #open the new window for the next results in this line
        if (self.sectorIndexInLine > 0):
            print("still working in current line")
            #decrement sectorIndexInLine since we are traversing from back to front (since top levels are in the "back" at the rightmost position)
            innerProcess = ProcessWindow(self.currentRow, self.sectorIndexInLine-1)
            print(self.currentRow)
            print(self.sectorIndexInLine)
            innerProcess.window.show_all()
            self.window.destroy()
        elif (self.currentRow < len(spaLinks)):
            print("current line finished, performing calculations")
            #perform the calculations for the items in this row
            #if the calculations fail, increment the fail counter and ask the user to re-enter complexity/uncertainty data
            #and try these calculations again
            if (True): #calculation fails

                #TODO: After a failed calculation, we go back and let the user re-enter data to try again for this line of the file
                #if the calculation for the line succeeds then we move on, also store the data that we get for each top-level/inner sector for each line for the sake of returning to if it reappears in subsequent lines
                #TODO: determine storage method for data
                self.failCount += 1
                while(self.failCount < 5 and not self.acceptable ):
                    #perform calculations and check failCount
                    calc = 0
                    self.failCount += 1

            if ( self.acceptable):

                print("moved to next line of file")
                #reset parameters to process the next row
                #if calculation for this row was within parameters
                self.sectorNumInLine = 0
                topLevelProcess = ProcessWindow(self.currentRow+1, len(spaLinks[self.currentRow+1]))
                self.window.destroy()
                topLevelProcess.window.show_all()
            #otherwise do nothing calculations have failed so print this to the screen and close the window
            else:
                print("successive fail limit of {} exceeded, exiting".format(self.failCount))
                self.window.destroy()
                skipWindow = SkipWindow(self.currentRow, len(spaLinks[self.currentRow]))
                skipWindow.window.show_all()
        '''


class SkipWindow:


    #constructor takes a list of tuples which are the names and amounts, this list is left empty if nothing is given
    def __init__(self, row, index):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("skip_window.glade")
        self.builder.connect_signals(self)
        self.currentRow = row
        self.SectorIndexInRow = index

        self.window = self.builder.get_object("skip_window")
        self.window.show_all()

    def onDeleteWindow(self, *args):
        self.window.destroy()
	Gtk.main_quit(*args)
        sys.exit()
        print("skip window delete-event signal")

    def on_skip_yes_clicked(self, button):
        #destroy the window and quit
        self.window.destroy()
        Gtk.main_quit()

    def on_skip_no_clicked(self, button):
        #re-open a database window
        new_dbwindow = ProcessWindow(self.currentRow, self.SectorIndexInRow)
        self.window.destroy()
        new_dbwindow.window.show_all()

'''
#while going through a line in the SPA results file, we can consider the sector numbers to alternate in an "outer level"
#and "inner level" fashion, so for the line 22-248-380, the order would be 380 (top) -> 248 (inner) ; 248 (top) -> 22 (inner)
class DatabaseResultsWindow:

    
    #constructor takes a list of tuples which are the names and amounts, this list is left empty if nothing is given
    def __init__(self, link1, link2):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("databaseresults.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("database_results")
        self.title = self.builder.get_object("label1")

        # name and amount labels
        self.firstResultName = self.builder.get_object("firstResultName")
        self.firstResultAmount = self.builder.get_object("firstResultAmount")
        self.secondResultName = self.builder.get_object("secondResultName")
        self.secondResultAmount = self.builder.get_object("secondResultAmount")
        self.thirdResultName = self.builder.get_object("thirdResultName")
        self.thirdResultAmount = self.builder.get_object("thirdResultAmount")
        self.fourthResultName = self.builder.get_object("fourthResultName")
        self.fourthResultAmount = self.builder.get_object("fourthResultAmount")
        self.fifthResultName = self.builder.get_object("fifthResultName")
        self.fifthResultAmount = self.builder.get_object("fifthResultAmount")
        # name and amount text fields
        self.manualEntryName = self.builder.get_object("manualEntryName")
        self.manualEntryAmount = self.builder.get_object("manualEntryAmount")
        
        # radio buttons
        self.firstResultButton = self.builder.get_object("firstResultSelectButton")
        self.secondResultButton = self.builder.get_object("secondResultSelectButton")
        self.thirdResultButton = self.builder.get_object("thirdResultSelectButton")
        self.fourthResultButton = self.builder.get_object("fourthResultSelectButton")
        self.fifthResultButton = self.builder.get_object("fifthResultSelectButton")
        self.manualEntryButton = self.builder.get_object("manualEntrySelectButton")

        self.resultNames = [self.firstResultName, self.secondResultName, self.thirdResultName, self.fourthResultName, self.fifthResultName, self.manualEntryName]
        self.resultAmounts = [self.firstResultAmount, self.secondResultAmount, self.thirdResultAmount, self.fourthResultAmount, self.fifthResultAmount, self.manualEntryAmount]

        
        #if len(namesAndAmounts) == 0:
            #namesAndAmounts = self.fruitsAndPrices #set the list to be this default if namesAndAmounts aren't given
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
Gtk.main()

process = 0
inner = 0
viewed = [] # keeps track of codes that have already been updated by user
spaLinks = getSPAlinks() # line by line links of codes in SPA results

# read each line of the SPA results
for x in range(len(spaLinks)):
    links = spaLinks[x]
    print("SPA links: "+str(links))
    # read each link in the line
    for y in range(len(links)):
        print("link: "+str(links[-y-1]))
        if links[-y-1] not in viewed:
            viewed.append(links[-y-1])
            process = ProcessWindow(links[-y-1])
            process.window.show_all()
            Gtk.main()
            while not process.onContinueClicked:
                t = 0 # do nothing
            # add process.results to matrix
            '''
            if y > 0:
                inner = DatabaseResultsWindow(links[-y-1],links[-y])
                inner.window.show_all()
                while not inner.onContinueClicked:
                    t = 0 # do nothing
            
#spaLinks is a list of lists, where each sublist is a line of the spa file
#print(spaLinks)

            '''
