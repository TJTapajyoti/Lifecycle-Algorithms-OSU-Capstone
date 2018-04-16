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

# Get the name of the process for code 'c'
def getName(cTn,c):
    name = 0
    for x in cTn:
        if x[0] == c:
            name = x[1]
    return name

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
        global limit3
        limit3 = self.builder.get_object("entry3").get_text()
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

        # search entry & button
        self.searchEntry = self.builder.get_object("searchEntry")
        self.searchButton = self.builder.get_object("searchButton")
        
        # set title and get top 5 results
        naics = getCode(link)
        name = getDescr(link)
        self.title.set_text("Process: "+name+" ("+str(naics)+")")
        description = [name]
        print(description)
        self.results = d.top5Processes(description)
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
        print("toggle button 1 clicked")
    
    def on_radiobutton2_toggled(self, button):
        self.toggle = 2
        print("toggle button 2 clicked")
       
    def on_radiobutton3_toggled(self, button):
        self.toggle = 3
        print("toggle button 3 clicked")
 
    def on_radiobutton4_toggled(self, button):
        self.toggle = 4
        print("toggle button 4 clicked")

    def on_radiobutton5_toggled(self, button):
        self.toggle = 5
        print("toggle button 5 clicked")

    def on_radiobutton6_toggled(self, button):
        self.toggle = 6
        print("toggle button 6 clicked")

    def onDeleteWindow(self, *args):
        self.window.destroy()
	Gtk.main_quit(*args)
        sys.exit()
        print("delete-event signal happened for ProcessWindow class")

    def on_searchButton_clicked(self,button):
        description = [self.searchEntry.get_text()]
        self.results = d.top5Processes(description)
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
        print("User selected "+str(self.results))
        self.window.destroy()
        Gtk.main_quit()

    
        
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


#while going through a line in the SPA results file, we can consider the sector numbers to alternate in an "outer level"
#and "inner level" fashion, so for the line 22-248-380, the order would be 380 (top) -> 248 (inner) ; 248 (top) -> 22 (inner)
class InputWindow:

    # outer=name of process, inner=spa code of input
    def __init__(self, outer, inner):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("inputWindow.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("database_results")
        self.title = self.builder.get_object("label1")
        self.toggle = 6
        
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

        # search entry & button
        self.searchEntry = self.builder.get_object("searchEntry")
        self.searchButton = self.builder.get_object("searchButton")
        
        self.resultNames = [self.firstResultName, self.secondResultName, self.thirdResultName, self.fourthResultName, self.fifthResultName]
        self.resultAmounts = [self.firstResultAmount, self.secondResultAmount, self.thirdResultAmount, self.fourthResultAmount, self.fifthResultAmount] 
        self.buttonList = [self.firstResultButton, self.secondResultButton, self.thirdResultButton, self.fourthResultButton, self.fifthResultButton, self.manualEntryButton]

        # set title and get top 5 results
        self.title.set_text("Input: "+inner+"\nIn Process: " + str(outer))
        self.results = []
        try:
            self.process = d.Process(outer)
            self.results = self.process.top5Inputs([inner])
        except:
            print("Manually entered process name")
        

        # populate name and amount fields with top 5 results for first line
        i = 0
        for x in self.resultNames:
            try:
                x.set_text(str(self.results[i][0]))
            except:
                x.set_text("...")
            i += 1
        i = 0
        for y in self.resultAmounts:
            try:
                y.set_text(str(self.results[i][2]))
            except:
                y.set_text("...")
            i += 1
        
    def on_radiobutton1_toggled(self, button):
        print("toggle button 1 clicked")
        self.toggle = 1
 
    def on_radiobutton2_toggled(self, button):
        print("toggle button 2 clicked")
        self.toggle = 2

    def on_radiobutton3_toggled(self, button):
        print("toggle button 3 clicked")
        self.toggle = 3
        
    def on_radiobutton4_toggled(self, button):
        print("toggle button 4 clicked")
        self.toggle = 4

    def on_radiobutton5_toggled(self, button):
        print("toggle button 5 clicked")
        self.toggle = 5
        
    def on_radiobutton6_toggled(self, button):
        print("toggle button 6 clicked")
        self.toggle = 6
        
    def onDeleteWindow(self, *args):
        self.window.destroy()
	Gtk.main_quit(*args)
        sys.exit()
        print("delete-event signal happened for ProcessWindow class")
        
    def onManualEntryDataChanged(self, entry):
        #set the manual entry radio button to be active
        self.manualEntryButton.set_active(True)

    def on_searchButton_clicked(self,button):
        description = [self.searchEntry.get_text()]
        try:
            self.results = self.process.top5Inputs(description)
            i = 0
            for x in self.resultNames:
                try:
                    x.set_text(str(self.results[i][0]))
                except:
                    x.set_text("...")
                i += 1
            i = 0
            for y in self.resultAmounts:
                try:
                    y.set_text(str(self.results[i][2]))
                except:
                    y.set_text("...")
                i += 1
        except:
            error = self.builder.get_object("label5")
            error.set_text("Manually entered process name. Cannot search for terms.")
            print("Manually entered process name")
        
            
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
        print("User selected: "+str(self.results[0]))
        self.window.destroy()
        Gtk.main_quit()


# Main

limits = limitsWindow()
Gtk.main()

pWin = 0
inner = 0
viewed = [] # keeps track of codes that have already been updated by user
spaLinks = getSPAlinks() # line by line links of codes in SPA results
codeToName = [] # list of tuples containing spa codes and their corresponding names

# read each line of the SPA results
for x in range(len(spaLinks)):
    links = spaLinks[x]
    print("\nSPA links: "+str(links))
    # read each link in the line
    for y in range(len(links)):
        print("link: "+str(links[-y-1]))
        
        if links[-y-1] not in viewed:
            viewed.append(links[-y-1])
            pWin= ProcessWindow(links[-y-1])
            pWin.window.show_all()
            Gtk.main()
            while not pWin.onContinueClicked:
                t = 0 # do nothing
            name = pWin.results
            codeToName.append([links[-y-1],name])
            #print(codeToName)
            if y > 0:
                #print("process input window")
                outer = getName(codeToName,links[-y])
                iWin = InputWindow(outer,name)
                iWin.window.show_all()
                Gtk.main()
                while not iWin.onContinueClicked:
                    t = 0 # do nothing
                    # add inner.results to matrix
                #print('exited input window')
                    
#spaLinks is a list of lists, where each sublist is a line of the spa file
#print(spaLinks)

