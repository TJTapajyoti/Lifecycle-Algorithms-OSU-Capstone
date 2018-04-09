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
        #print(numbers)
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

        #items used during the calculations process
        self.failCount = 0
        self.acceptable = False

        #NOTE, indexing within row for calculations/model building happens by going from right to left,
        #so the index in the line needs to be relative to the back of the list
        self.currentRow = row
        self.sectorIndexInLine = len(spaLinks[self.currentRow]) - 1

        # set title and get top 5 results
        print(i)
        link = spaLinks[self.currentRow][self.sectorIndexInLine]
        preceding = link

        #reverse the row before we work with it so that the indexes line up 
        spaLinks[row].reverse()

        print(spaLinks[row])
        spaLinks[row].reverse()
        print(link)
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
        print("delete-event signal happened for ProcessWindow class")    
    def onManualEntryDataChanged(self, entry):
        #set the manual entry radio button to be active
        self.manualEntryButton.set_active(True)
        
    def onContinueClicked(self, button):
        # if there are inputs to the process, open up the top 5 inputs window. Else if there are more processes in the link, open up a new process window. Else perform calculations

        
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

            if (self.acceptable):

                print("moved to next line of file")
                #reset parameters to process the next row
                #if calculation for this row was within parameters
                self.sectorNumInLine = 0
                topLevelProcess = ProcessWindow(self.currentRow+1, len(spaLinks[self.currentRow+1]))
                self.window.destroy()
                topLevelProcess.show_all()
            #otherwise do nothing calculations have failed so print this to the screen and close the window
            else:
                print("successive fail limit of {} exceeded, exiting".format(self.failCount))
                self.window.destroy()
                Gtk.main_quit()















#============================ OLD

#while going through a line in the SPA results file, we can consider the sector numbers to alternate in an "outer level"
#and "inner level" fashion, so for the line 22-248-380, the order would be 380 (top) -> 248 (inner) ; 248 (top) -> 22 (inner)
class InnerProcessWindow:
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

#spaLinks is a list of lists, where each sublist is a line of the spa file
#print(spaLinks)

