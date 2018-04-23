#!/usr/local/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import databaseWrapper as d
import model_generator as mg
import csv
import sys
import math
from numpy.linalg import inv

# Global variables
comp = 0
unce = 0
tol = 0

def runLine(links):
    global modelGenerator
    global codeToName
    
    # read each link in the line
    for y in range(len(links)):
        print("link: "+str(links[-y-1]))
        # read from right to left at the end
        if not modelGenerator.has_process(links[-y-1]):
            #viewed.append(links[-y-1])
            # Open Process Name Selector Window
            pWin = ProcessWindow(links[-y-1])
            pWin.window.show_all()
            Gtk.main()
            while not pWin.onContinueClicked:
                pass  #wait for user
            
            # add outer results to matrix
            name = pWin.results[0]
            modelGenerator.add_process(links[-y-1],pWin.results[1],pWin.results[3])
            codeToName.append([links[-y-1],name])
            paramWin = ParametersWindow(name)
            paramWin.window.show_all()
            Gtk.main()
            while not paramWin.onSubmitClicked:
                pass #wait for user
            
            # add uncertainty and complexity values
            modelGenerator.set_process_unc_and_comp(links[-y-1],paramWin.processUncertainty,paramWin.envUncertainty,paramWin.processComplexity)

        if y > 0:
            if not modelGenerator.has_process_input(links[-y],links[-y-1]):
                outer = getName(codeToName,links[-y])
                name = getName(codeToName,links[-y-1])
                iWin = InputWindow(outer,name)
                iWin.window.show_all()
                Gtk.main()
                while not iWin.onContinueClicked:
                    pass #wait for user
                
                # add inner results to matrix
                modelGenerator.add_process_input(links[-y],links[-y-1],float(iWin.results[2]))


# displays the matrix on a csv file
def displayMatrix(model):
    with open('final_matrix.csv','wb') as csvfile:
        writer = csv.writer(csvfile,delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in model:
            writer.writerow(i)
            
                
# Get the NAICS code from sectorsCodes csv file
def getCode(num):
    naics = 0
    with open('SectorsCodes.csv','rb') as f:
        sectorCodes = csv.reader(f)
        for row in sectorCodes:
            if row[0] == num:
                naics = row[1]
    return naics


# Get the industry description from sectorsCodes csv file
def getDescr(num):
    descr = ""
    if sys.version_info[0] < 3: 
        infile = open('SectorsCodes.csv', 'rb')
    else:
        infile = open('SectorsCodes.csv', 'r', newline='', encoding='utf8')

    with infile as f:
    # with open('SectorsCodes.csv','rb') as f:
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
       
    def onContinue(self, button):
        errorMessage = self.builder.get_object("error")
        try:
            global comp
            comp = self.builder.get_object("entry1").get_text()
            global unce
            unce = self.builder.get_object("entry2").get_text()
            global tol
            tol = self.builder.get_object("entry3").get_text()
            self.window.destroy()
            Gtk.main_quit()
        except:
            errorMessage.set_text("Invalid Entry")
        

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
        
        # name, amount, and units labels
        self.firstResultName = self.builder.get_object("firstResultName")
        self.firstResultAmount = self.builder.get_object("firstResultAmount")
        self.firstResultUnit = self.builder.get_object("firstResultUnit")
        self.secondResultName = self.builder.get_object("secondResultName")
        self.secondResultAmount = self.builder.get_object("secondResultAmount")
        self.secondResultUnit = self.builder.get_object("secondResultUnit")
        self.thirdResultName = self.builder.get_object("thirdResultName")
        self.thirdResultAmount = self.builder.get_object("thirdResultAmount")
        self.thirdResultUnit = self.builder.get_object("thirdResultUnit")        
        self.fourthResultName = self.builder.get_object("fourthResultName")
        self.fourthResultAmount = self.builder.get_object("fourthResultAmount")
        self.fourthResultUnit = self.builder.get_object("fourthResultUnit")
        self.fifthResultName = self.builder.get_object("fifthResultName")
        self.fifthResultAmount = self.builder.get_object("fifthResultAmount")
        self.fifthResultUnit = self.builder.get_object("fifthResultUnit")        
        # name, amount, units, and Co2 manual entry text fields
        self.manualEntryName = self.builder.get_object("manualEntryName")
        self.manualEntryAmount = self.builder.get_object("manualEntryAmount")
        self.manualEntryUnit = self.builder.get_object("manualEntryUnit")  
        self.manualEntryCo2 = self.builder.get_object("manualEntryCo2")
        
        # radio buttons
        self.firstResultButton = self.builder.get_object("firstResultSelectButton")
        self.secondResultButton = self.builder.get_object("secondResultSelectButton")
        self.thirdResultButton = self.builder.get_object("thirdResultSelectButton")
        self.fourthResultButton = self.builder.get_object("fourthResultSelectButton")
        self.fifthResultButton = self.builder.get_object("fifthResultSelectButton")
        self.manualEntryButton = self.builder.get_object("manualEntrySelectButton")

        # lists of names, amounts, units, and buttons objects
        self.resultNames = [self.firstResultName, self.secondResultName, self.thirdResultName, self.fourthResultName, self.fifthResultName]
        self.resultAmounts = [self.firstResultAmount, self.secondResultAmount, self.thirdResultAmount, self.fourthResultAmount, self.fifthResultAmount]
        self.resultUnits = [self.firstResultUnit, self.secondResultUnit, self.thirdResultUnit, self.fourthResultUnit, self.fifthResultUnit] 
        self.buttonList = [self.firstResultButton, self.secondResultButton, self.thirdResultButton, self.fourthResultButton, self.fifthResultButton, self.manualEntryButton]
        
        # search entry & button
        self.searchEntry = self.builder.get_object("searchEntry")
        self.searchButton = self.builder.get_object("searchButton")
        
        # set title and get top 5 results
        naics = getCode(link)
        name = getDescr(link)
        self.title.set_text("Process: "+name+" (NAICS: "+str(naics)+")")
        self.manualEntryName.set_text(name)
        description = [name]
        print(description)
        self.results = d.top5Processes(description)
        self.toggle = 6
        
        # populate name, amount, and units fields with top 5 results 
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
                y.set_text(str(self.results[i][1]))
            except:
                y.set_text("...")
            i += 1
        i = 0
        for z in self.resultUnits:
            try:
                z.set_text(str(self.results[i][2]))
            except:
                z.set_text("...")
            i += 1

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

    def on_searchButton_clicked(self,button):
        description = [self.searchEntry.get_text()]
        self.results = d.top5Processes(description)
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
                y.set_text(str(self.results[i][1]))
            except:
                y.set_text("...")
            i += 1
        i = 0
        for z in self.resultUnits:
            try:
                z.set_text(str(self.results[i][2]))
            except:
                z.set_text("...")
            i += 1
    '''    
    def onManualEntryDataChanged(self, entry):
        #set the manual entry radio button to be active
        self.manualEntryButton.set_active(True)
    '''    
    def onContinueClicked(self, button):
        if self.toggle < 6:
            for i in range(5):
                if self.toggle == i+1:
                    self.results = self.results[i]
                    try:
                        # print(d.Process(self.results[i][0]).carbonDioxide())
                        self.results.append(d.Process(self.results[i][0]).carbonDioxide())
                    except:
                        self.results.append(0)
        elif self.toggle == 6:
            self.results = [self.manualEntryName.get_text()]+[self.manualEntryAmount.get_text()]+[self.manualEntryUnit.get_text()]+[self.manualEntryCo2.get_text()]
        print("User selected: "+str(self.results[0])+", Amount: "+str(self.results[1])+" "+str(self.results[2]))
        self.window.destroy()
        Gtk.main_quit()

    
        
class SkipWindow:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("skip_window.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("skip_window")
        self.button = 0
        # self.window.show_all()

    def on_button1_clicked(self, button):
        self.button = 1
        self.window.destroy()
        Gtk.main_quit(*args)

    def on_button2_clicked(self, button):
        #destroy the window and go to the threshold re-entry for each process in the line
        self.button = 2
        self.window.destroy()
        Gtk.main_quit()

    def onDeleteWindow(self, *args):
        self.window.destroy()
        Gtk.main_quit(*args)
        sys.exit()
        
#while going through a line in the SPA results file, we can consider the sector numbers to alternate in an "outer level"
#and "inner level" fashion, e.g. the line 22-248-380, we get the info for 380 as a top level, then the info for 248 as a top level and as an input to 380, then, we get the info for 22 as a top level and as an input to the process 248. Then we perform the calculations for the model, try again if the values aren't within the acceptable threshold and quit if it fails 5 times successively.
class InputWindow:

    # outer=name of process, inner=spa code of input
    def __init__(self, outer, inner):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("inputWindow.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("database_results")
        self.title = self.builder.get_object("label1")
        self.toggle = 6
        
        # name, amount, and units labels
        self.firstResultName = self.builder.get_object("firstResultName")
        self.firstResultAmount = self.builder.get_object("firstResultAmount")
        self.firstResultUnit = self.builder.get_object("firstResultUnit")
        self.secondResultName = self.builder.get_object("secondResultName")
        self.secondResultAmount = self.builder.get_object("secondResultAmount")
        self.secondResultUnit = self.builder.get_object("secondResultUnit")
        self.thirdResultName = self.builder.get_object("thirdResultName")
        self.thirdResultAmount = self.builder.get_object("thirdResultAmount")
        self.thirdResultUnit = self.builder.get_object("thirdResultUnit")        
        self.fourthResultName = self.builder.get_object("fourthResultName")
        self.fourthResultAmount = self.builder.get_object("fourthResultAmount")
        self.fourthResultUnit = self.builder.get_object("fourthResultUnit")
        self.fifthResultName = self.builder.get_object("fifthResultName")
        self.fifthResultAmount = self.builder.get_object("fifthResultAmount")
        self.fifthResultUnit = self.builder.get_object("fifthResultUnit")        
        # name, amount, and units manual entry text fields
        self.manualEntryName = self.builder.get_object("manualEntryName")
        self.manualEntryAmount = self.builder.get_object("manualEntryAmount")
        self.manualEntryUnit = self.builder.get_object("manualEntryUnit")               
        
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
        self.resultUnits = [self.firstResultUnit, self.secondResultUnit, self.thirdResultUnit, self.fourthResultUnit, self.fifthResultUnit] 
        self.buttonList = [self.firstResultButton, self.secondResultButton, self.thirdResultButton, self.fourthResultButton, self.fifthResultButton, self.manualEntryButton]

        # set title and get top 5 results
        self.title.set_text("Input: "+str(inner)+"\nIn Process: " + str(outer))
        self.manualEntryName.set_text(inner)
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
        i = 0
        for z in self.resultUnits:
            try:
                z.set_text(str(self.results[i][3]))
            except:
                z.set_text("...")
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
                    y.set_text(str(self.results[i][2])) #index 1 is the score value
                except:
                    y.set_text("...")
                i += 1
            i = 0
            for z in self.resultUnits:
                try:
                    z.set_text(str(self.results[i][3]))
                except:
                    z.set_text("...")
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
            self.results = [self.manualEntryName.get_text()]+[""]+[self.manualEntryAmount.get_text()]+[self.manualEntryUnit.get_text()]
        print("User selected: "+str(self.results[0])+", Amount: "+str(self.results[2])+" "+str(self.results[3]))
        self.window.destroy()
        Gtk.main_quit()

#Window to be used to enter process and env uncertainty + complexity for each process in a line after the line has been processed
#but before the calculations have been performed
class ParametersWindow:

    def __init__(self,name):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("process_parameters2.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("process_parameters")
        self.builder.get_object("title_label").set_text(name)
        
    def onSubmitClicked(self, button):
        #get the text from the entries and open up the skip window
        self.processUncertainty = float(self.builder.get_object("processUncertaintyData").get_text())
        self.envUncertainty = float(self.builder.get_object("envUncertaintyData").get_text())
        self.processComplexity = float(self.builder.get_object("complexityData").get_text())
        print("Process Uncertainty: "+str(self.processUncertainty))
        print("Process EnvUncertainty: "+str(self.envUncertainty))
        print("Process Complexity: "+str(self.processComplexity))
        self.window.destroy()
        Gtk.main_quit() 
    
    def onDeleteWindow(self, *args):
        self.window.destroy()
        Gtk.main_quit(*args)
        sys.exit()
        
#Added: 4/16/18, pulled up when a line has been processed, if the user wishes to continue building the model
#click continue, otherwise, click finish and the program will finalize the current model and exit
class FinishWindow:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("finish_window.glade")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("finish_window")
        self.window.show_all()


    def on_continue_button_clicked(self, button):
        #get the next line and process each of the processes on that line as before
        #that is, open a new db window and loop back again
        self.window.destroy()
        new_db_window = DatabaseResultsWindow()
        Gtk.main()
    def on_finish_button_clicked(self, button):
        #finalize model stuff and exit the program
        self.window.destroy()
        sys.exit()

    def onDeleteWindow(self, *args):
        self.window.destroy()
        Gtk.main_quit(*args)
        sys.exit()


#dbwindow = DatabaseResultsWindow()
#Gtk.main()



# Main
limits = limitsWindow()
Gtk.main()
print("Complexity: "+str(comp)+" Uncertainty: "+str(unce)+" Tolerance: "+str(tol))

modelGenerator = mg.Final_Model_Generator(comp,unce, tol)
spaLinks = getSPAlinks() # line by line links of codes in SPA results
codeToName = [] # list of tuples containing spa codes and their corresponding names the user selects

# read each line of the SPA results
for x in range(len(spaLinks)):
    links = spaLinks[x]
    print("\nSPA links: "+str(links))
    runLine(links)
    
    exit_bool = False
    while not exit_bool:
        value = modelGenerator.create_new_matrix_and_calculate()
        print('got back value {}'.format(value))
        if value is False:
            print("Failed Calculation")
            skipWin = SkipWindow()
            skipWin.window.show_all()
            Gtk.main()
            while skipWin.button < 1:
                pass #user makes decision to reenter process info or display most recent matrix
        
            if skipWin.button == 1:
                modelGenerator.clear_unfinalized_data()
                runLine(links)
            elif skipWin.button == 2:
                #modelGenerator.get_most_recent_model()
                modelGenerator.finalize()
                #display results
                displayMatrix(modelGenerator.get_most_recent_model().matrix)
                exit_bool = True
        elif value is True:
            print("Passed Calculation")
            modelGenerator.finalize()
            break
            # exit_bool = False
        elif value == "exit":
            #modelGenerator.get_most_recent_model()
            # modelGenerator.finalize()
            #display results
            displayMatrix(modelGenerator.get_most_recent_model().matrix)
            exit_bool = True
    if exit_bool:
        break
                    

# modelGenerator.finalize()
#display results
displayMatrix(modelGenerator.get_most_recent_model().matrix)

