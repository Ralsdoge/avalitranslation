from tkinter import messagebox
import os, sys
def absolute_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    if getattr(sys, 'frozen', False):  # running as .exe
        return os.path.join(os.path.dirname(sys.executable),relative_path)

    else:  # running as .py
        return relative_path

'''def writeIni(Rsection,Ratribute,Rvalue): #write saved settings to ini file #cannot write a single digit
    with open("settings.ini", "w") as file:
        rawData = file.read()
        #print(rawData,"\n------------------------")
        rawData = rawData.splitlines()
        curSection = ""
        count = 0
        for i in range(len(rawData)):
            #print(rawData[i])
            count += len(rawData[i])+1 #+1 is for newline character
            if "[" in rawData[i]:
                Section = rawData[i].replace("[","").replace("]","")
                curSection = Section
                if curSection == Rsection:
                    count -= len(rawData[i])
                    for k in range(len(rawData)-i+1):
                        #print(rawData[i+k],"  -  ",count," + ",len(rawData[i+k]))
                        #print(rawData[i+k].split("="))
                        count += len(rawData[i+k])+1 #+1 is for newline character

                        line = rawData[i+k].split("=")
                        if line[0] == str(Ratribute):
                            #print("FOUND: ",line[0],"   VALUE: ",line[1])
                            inLineCount = len(line[0])
                            file.seek(count-len(rawData[i+k]))
                            loi = file.read(len(rawData[i+k]))
                            print(loi)
                            file.seek(inLineCount)
                            file.write("1") ###FIGURE THIS OUT #r+b
                            print(loi)
                            file.close()
                            break
        print('exit')

    '''

def errorMsg(Title,Desc):  #Error: 
    messagebox.showerror(Title,Desc)
def infoMsg(Title,Desc): #Info
    messagebox.showinfo(Title, Desc)

    

def writeIni(Rsection,Ratribute,Rvalue):
    with open("settings.ini", "r+") as file:
        rawData = file.read()
        #print(rawData,"\n------------------------")
        rawDataS = rawData.splitlines()
        #print(rawDataS)
        curSection = ""
        count = 0
        for i in range(len(rawDataS)):
            #print(rawDataS[i])
            count += len(rawDataS[i])+1 #+1 is for newline character
            if "[" in rawDataS[i]:
                Section = rawDataS[i].replace("[","").replace("]","")
                curSection = Section
                if curSection == Rsection:
                    #count -= len(rawDataS[i])
                    for k in range(len(rawDataS)-i+1):
                        #print(k)
                        #print(rawDataS[i+k],"  -  ",count," + ",len(rawDataS[i+k]))
                        #print(rawDataS[i+k].split("="))
                        #count += len(rawDataS[i+k])+1 #+1 is for newline character
                        line = rawDataS[i+k].split("=")
                        if line[0] == str(Ratribute):
                            #print("FOUND: ",line[0],"   VALUE: ",line[1])
                            #inLineCount = len(line[0])
                            loi = file.read(len(rawDataS[i+k]))
                            #print(loi)
                            #print(str(line[0])+"="+Rvalue)
                            rawDataS[i+k] = str(str(line[0])+"="+Rvalue)
                            #print(loi)
                            joiner = '\n'
                            
                            result = joiner.join(rawDataS)
                            #print(result)
                            file.truncate(0) #clear file ##So fucking stupid
                            file.seek(0) #prevents Null value leak
                            file.write(result) #rewrite
                            file.close() #Close file
                            break
    curSection = ""
    
    '''for i in range(len(rawData)):
        print(rawData[i])
        if "[" in rawData[i]:
            Section = rawData[i].replace("[","").replace("]","")
            curSection = Section
            if curSection == Rsection:
                for k in range(len(rawData)-i+1):
                    line = rawData[i].split("=")
                    if line[0] == str(Ratribute):
                        print("FOUND: ",line[0],"   VALUE: ",line[1])
                        #print(line[1])
        else:
            pass
    '''

def readIni(RSection,Option): #read the ini file and return value and line
    rawData = open("settings.ini").read().splitlines()
    curSection = ""
    for i in range(len(rawData)):
        stripedDataLine =rawData[i].strip()
        if stripedDataLine == "":
            pass
        elif "[" in stripedDataLine:
            Section = stripedDataLine.replace("[","").replace("]","")
            curSection = Section
            #print(curSection)
        else:
            if curSection == RSection:
                line = stripedDataLine.split("=")
                #print('VALID:',end=' ')
                #print(line)
                if line[0].strip() == str(Option.strip()):
                    #print("FOUND: ",line[1])
                    if "//" in line[1]:
                        line = line[1].split("//")
                        #print('line(split):',line)
                        line[1] = line[0]
                    #print('line[1]:',line[1])
                    return line[1],i+1
                #print(rawData[i],end=" -> ")
                #print("(",curSection,") ",line)
                #print(rawData[i])
                #print(curSection,line)
def exitPrgrm():
    sys.exit()
def resetini():
    debug = 0 #If set to 1 then it bypasses this func when its called.
    if debug == 1:
        print('DEBUG MODE ON resetini() line 134')
        return 'debug'
    iniBackupOLD = '[Theme]\n//Dont be detured by the ammount of colors you need to choose, I just wanted to ensure full customizeability. Most should be quite similar to another\nsetTheme=1 //Themes are selected in the program by index numbers\n    Light=[#f0f0f0,#000000,#fc850f,#000000,#ff3419,#fffafa,#d3d3d3,#ffffff] //1\n    Dark=[#1f1f1f,#ffffff,#fc850f,#ffffff,#ff3419,#fffafa,#d3d3d3,#ffffff] //2\n    customTheme1=[#5f1352,#ffffff,#ffffff,#ffffff,#ffffff,#2de2aa,] //Main, Text, Accent, Accent Text, ActiveAccent, ActiveAccentText, Textbox, Icons\n    customTheme2=[#333333,#333333,#333333,#333333,#333333,#333333,#333333,#333333] //Test all colors using theme\n    customTheme=[] //Main, Text, Accent, Accent Text, ActiveAccent, ActiveAccentText, Textbox, Icons\n[Translation]\nTableView = 0 //0-1 Visible by default\nEnglishView = 1 //0-1 Visible by default\n[Pronunciation]\nHpron=0 //0-5\nCchars=0 //0-6\nLastH=0 //0-4\nLastC=0 //0-5\n[Numbers]\nHV=0 //Horizontal&Vertical 0&1 respectivly\n'
    iniBackup = '[Theme]\n//Dont be detured by the ammount of colors you need to choose, I just wanted to ensure full customizeability. Most should be quite similar to another\nsetTheme=1\n    Light=[#f0f0f0,#000000,#fc850f,#000000,#ff3419,#fffafa,#d3d3d3,#ffffff,#f0f0f0,#000000] //1\n    Dark=[#1f1f1f,#ffffff,#fc850f,#ffffff,#ff3419,#fffafa,#d3d3d3,#ffffff,#f0f0f0,#000000] //2\ncustomTheme1=[#5f1352,#ffffff,#ffffff,#ffffff,#ffffff,#2de2aa,] \n    TestTheme=[#b800a7,#b800a7,#b800a7,#b800a7,#b800a7,#b800a7,#b800a7,#b800a7,#b800a7,#b800a7]\n    customTheme=[] //Main, Text, Accent, Accent Text, ActiveAccent, ActiveAccentText, Textbox, Icons, Button/Menu, Contrasting Button/Menu Text\n[Translation]\nTableView = 0 //0-1 Visible by default\nEnglishView = 1 //0-1 Visible by default\n[Pronunciation]\nHpron=0 //0-5\nCchars=0 //0-6\nLastH=0 //0-4\nLastC=0 //0-5\n[Numbers]\nHV=0 //Horizontal&Vertical 0&1 respectivly'
    exists=1
    eraseProtect=0
    status='Clear'
    try:
        file = open("settings.ini")#.read()#.splitlines()
    except:
        status = '"settings.ini" file did not exist. A new one was created automaticly.'
        exists = 0
    if exists == 0: 
        pass #if it does not exist skip renaming
    else: 
        file.close() #close file so we can rename it. We cant get here without opening the file 
        try: #since it does exist rename current one
            os.rename("settings.ini","settingsOLD.ini") #if it does reaname
        except Exception as e: 
            eraseProtect=1 #if we fail we dont want to destroy user data
            status = e + 'Please empty settingsOLD.ini of wanted data before deleting.' #store error for reporting
            #print(status)
    if eraseProtect == 1:
        pass #dont overwrite user's old file get to error reporting
    else:
        file = open("settings.ini", "w") #if successful in renaming, create a new settings.ini file
        file.write(str(iniBackup)) #and populate it
        file.close()
    if status == 'Clear':
        pass
    else: 
        errorMsg('Error',status)
    #save old file as settingsOLD.ini  #check availibility of .old
    #Restore original .ini with hardcoded backup in this function

def verifyiniIntegrity():
    debug = 0 #If set to 1 then it bypasses this func when its called.
    if debug == 1:
        print('DEBUG MODE ON verifyiniIntegrity() line 165')
        return 'debug'
    status = 'Correct'
    skip = 0
    #Check if file exists 
    try:
        rawData = open("settings.ini").read()#.splitlines()
    except:
        status = '"settings.ini" file did not exist. A new one was created automaticly.'
        skip = 1
    if skip == 0:
        #See if it has minimum amount of characters and linescontents
        rawData = open("settings.ini").read()#.splitlines()
        print('Length of "settings.ini":',len(rawData))
        if len(rawData) < 133:
            status = 'File missing info (character count check failed)'
        rawData = rawData.splitlines()
        print('# of lines in "settings.ini":',len(rawData))
        if len(rawData) < 12:
            status = 'File missing info (line count check failed)'
        #Checks go here any descrepicy will be identified and stored in status. Then shown in error message
    if status != 'Correct':
        resetini()
        errorMsg('Error opening "settings.ini"',status)
verifyiniIntegrity()

def retrieveTheme(Theme,line,checkValidity=0): #returns the currently selected theme as a list of hex values by default or validates that a theme is properly formated and alerts the user if not.
    if checkValidity == True: #with check validity set to 1: 
        char_list = ['#','0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','A','B','C','D','E','F']
        Theme = Theme #Value for set theme
        Theme = int(Theme)
        line = int(line) #Index for set theme
        #print('ENTER: retrieveTheme -',Theme,line,checkValidity)
        bottom = readIni("Translation","TableView") #I check where the bottom of the theme list is 
        #Debug
        #print("bottom:",bottom)
        #print('Theme:',Theme)
        #print('Line:',line)
        if (Theme+line > int(bottom[1])-1):
            print("Error: Invalid selection") #silent Error message Dont need to warn explicitly
            writeIni("Theme","setTheme",0)#set back to lowest value
            return(False)
        rawData = open("settings.ini").read().splitlines()

        themeLine = rawData[line+Theme-1]
        #print("themeLine:",themeLine)
        themeLine = themeLine.split("[")
        themeLine = themeLine[1].split("]")
        themeLine.pop(1)
        themeLine = themeLine[0].split(",")
        if len(themeLine) < 10:
            errorMsg("invalidCodeAmount","One or more hex codes in theme "+str(Theme)+" are not present. There should be 10 html color codes.")
            return False
        for i in range(0,10,1):
            if len(themeLine[i]) != 7:
                errorMsg("invalidLength","One or more hex codes in theme "+str(Theme)+" is an invalid length. There should be a # followed by 6 characters.")
                return False
            elif '#' not in themeLine[i]:
                errorMsg("missingHash","One or more hex codes in theme "+str(Theme)+" are missing their hash symbol.")
                return False
            for character in themeLine[i]:
                if character not in char_list:
                    errorMsg("invalidCharacter","One or more hex codes in theme "+str(Theme)+" cotains an invalid character. Hex values should only include the characters 0-9 and A-F.")
                    return False
        print("Selected Theme",str(Theme),"is valid.")
        return True
    else:
        Theme = int(Theme)
        line = int(line)

        rawData = open("settings.ini").read().splitlines()
        themeLine = rawData[line+Theme-1]
        themeLine = themeLine.split("[")

        themeLine = themeLine[1].split("]")
        themeLine.pop(1)        
        themeLine = themeLine[0].split(",")
        print("Using Theme",str(Theme)+":",themeLine)
        return themeLine

'''singer = readIni('Numerical','testParamater')
print(singer)
writeIni('Numerical','testParamater','1')
singer = readIni('Numerical','testParamater')
print(singer)'''
#Theme = readIni('Theme','setTheme')
#retrieveTheme(Theme[0],Theme[1],1)