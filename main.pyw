import pyglet
from tkinter import *
from PIL import ImageTk, Image
import GatherOptions as GO
import GatherRandChars as GRC 
import AvalianPronunciation as AP
import AvalianNumbers as AN
import random
import imageTinter as iT
import time
try:
    pyglet.font.add_file('avali-scratch.ttf')
except:
    GO.errorMsg('avali-scratch.ttf missing','The file "avali-scratch.ttf" is missing, please replace avali-scratch.ttf or reinstall program.')
    GO.exitPrgrm()
WindowRegister = []
GO.verifyiniIntegrity() #check on ini file
#Theme Loading
Theme = GO.readIni("Theme","setTheme") #Get theme from ini
try: 
    int(Theme[0])
except:
    GO.errorMsg('Illegal Character in setTheme','The setTheme option has been set to an invalid character. Please dont do this. \n\nIm tired of writing exceptions.')
    GO.writeIni("Theme","setTheme",'1')
    Theme = (1,Theme[1])
if int(Theme[0]) < 1:
    GO.writeIni("Theme","setTheme",'1')
    Theme = (1,Theme[1])

#print('Theme: ',Theme)
if not GO.retrieveTheme(Theme[0],Theme[1],1): #Validate 
    #print('not true Validation')
    if GO.retrieveTheme(1,Theme[1],1):
        Theme = GO.retrieveTheme(Theme[0],1) #Run theme through seperate function to populate global theme list
        GO.errorMsg("Error: Selected Theme Corupted","Selected Theme (Theme starting with: "+str(Theme[0])+") is corrupt(see previous errors). Launching program with defualt theme(Theme 1) and setting to default in .ini file.") 
        #print('1LL:',Theme)
        GO.writeIni("Theme","setTheme",'1')#set back to lowest value
    else:
        #print("Defaulting to hardcoded theme, file fallback corupt(see errors)")
        GO.errorMsg('Error: Defaulting Theme','Defaulting to hardcoded theme, ini file themes are corupt(see previous errors)')
        #print('2LL:',Theme)
        Theme = ['#f0f0f0','#000000','#fc850f','#000000','#ff3419','#fffafa','#d3d3d3','#ffffff','#f0f0f0','#000000']

        #print('3LL:',Theme)
        GO.resetini() #Trigger .ini Reset
else: 
    #print("Start Else statement")
    Theme = GO.retrieveTheme(Theme[0],Theme[1]) #Run theme through seperate function to populate global theme list
#print('4LL:',Theme)
def AddWindowToRegister(win,type): #Add a new window to the Register, Has adorable abreviation "AWTR"
    date = time.time()
    Entry = [win,type,date]
    WindowRegister.append(Entry)
    win.iconbitmap("Images/AppIcon.ico")
    print(WindowRegister,'-AWtR line 53')## DEBUG
    return date

def RemoveWindowFromRegister(win,date,type): #Remove a specific window from the directory
    for i in range(len(WindowRegister)):
        if date == WindowRegister[i][2]:
            if type == WindowRegister[i][1]:
                if WindowRegister.pop(i):
                    win.destroy()
                    print(WindowRegister,'-RWfR line 62')## DEBUG
                    return(True)
    win.destroy()
    GO.errorMsg('Error: Failed to remove closed window from Register','Dont worry nothing bad. If you have trouble opening a window please restart the application.')
    return(False)

def CheckWindowRegister(type='X'): #Check if a type of window exists in the Register
    typeCount = 0
    for i in range(len(WindowRegister)):
        #print("Checking for,'"+str(type)+"':",WindowRegister[i],'---',WindowRegister[i][1]) #Debug found bug checking WindowRegister[i][2] (Datecode) instead of WindowRegister[i][1] (window type)
        if type == WindowRegister[i][1]:
            typeCount +=1
    if type == 'P' or type == 'O' or type == 'C' or type == 'N':
        if typeCount >= 1:
            return(False)
    if type == 'T' or type == 'X':
        if typeCount >= 3:
            return(False)
    return(True)

def WindowToTop(type='X'): #Move a type of window to the top
    #if type == 'P' or type == 'O' or type == 'C' or type == 'N':
    #if not CheckWindowRegister(type): #I cant tell you why this works #You find it was never nececary to begin with
    for i in range(len(WindowRegister)):
        #Find stupid window object
        if WindowRegister[i][1] == type:
            WindowRegister[i][0].lift() #does the same thing but I am told to use the other.. perhaps different across systems
            #WindowRegister[i][0].attributes("-topmost",True)
            #WindowRegister[i][0].attributes("-topmost",False)
                    
    #else:
    #    print('AHHHh')

def WindowRegistration(type='X'):
    print("Window Request Landed: Type("+str(type)+")",end='  Response: ')
    if type == 'M':
        WindowToTop('M')
    if type == 'P':
        print(CheckWindowRegister('P'))
        if CheckWindowRegister('P'):
            createPronunciationWin()
        
    if type == 'O':
        print(CheckWindowRegister('O'))
        if CheckWindowRegister('O'):
            createOptionsWin()
        else:
            WindowToTop('O')
    if type == 'C':
        print(CheckWindowRegister('C'))
        if CheckWindowRegister('C'):
            createCreditsWin()
        else:
            WindowToTop('C')
    if type == 'N':
        print(CheckWindowRegister('N'))
        if CheckWindowRegister('N'):
            createNumbersWin()
        else:
            WindowToTop('P')
    if type == 'T':
        print(CheckWindowRegister('T'))
        if CheckWindowRegister('T'):
            createFontTranslationWin()
        else:
            WindowToTop('T') #caused other to front actions things to break
    if type == 'X':
        print('Undocumented window type.')

class HoverButton(Button): #Used for the sidebar menu buttons
    def __init__(self, master, **kw):
        Button.__init__(self,master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

class SidebarMenu(): #Class to create the menubar 
    MenuImgs = [] 
    def __init__(self,winObj,border_frame): #Creates a menubar in the specified window
        #Create Menu Sidebar    
        Sidebar = Frame(border_frame,background="#f0f0f0",borderwidth= "0")
            ##IN
        MB0 = HoverButton(Sidebar,text="Main Menu",image=SidebarMenu.MenuImgs[0], command=lambda: WindowRegistration('M'),relief=FLAT,foreground=Theme[5],background=Theme[2],activebackground=Theme[4],height=60,width=0) #em W=0 H=2
        MB1 = HoverButton(Sidebar,text="Font Trans.",image=SidebarMenu.MenuImgs[1], command=lambda: WindowRegistration('T'),relief=FLAT,foreground=Theme[5],background=Theme[2],activebackground=Theme[4],height=60,width=0)
        MB2 = HoverButton(Sidebar,text="Number Trans.",image=SidebarMenu.MenuImgs[2], command=lambda: WindowRegistration('N'),relief=FLAT,foreground=Theme[5],background=Theme[2],activebackground=Theme[4],height=60,width=0)
        MB3 = HoverButton(Sidebar,text="Pronunciation",image=SidebarMenu.MenuImgs[3], command=lambda: WindowRegistration('P'),relief=FLAT,foreground=Theme[5],background=Theme[2],activebackground=Theme[4],height=60,width=0)
        MB4 = HoverButton(Sidebar,text="Options",image=SidebarMenu.MenuImgs[4], command=lambda: WindowRegistration('O'),relief=FLAT,foreground=Theme[5],background=Theme[2],activebackground=Theme[4],height=60,width=0)
        MB5 = HoverButton(Sidebar,text="Credits",image=SidebarMenu.MenuImgs[5], command=lambda: WindowRegistration('C'),relief=FLAT,foreground=Theme[5],background=Theme[2],activebackground=Theme[4],height=60,width=0)
        #SideBorder = Canvas(background=Theme[3]) #Maybe not
        MB0.grid(column=0,row=1,sticky='nesw')
        MB1.grid(column=0,row=2,sticky='nesw')
        MB2.grid(column=0,row=3,sticky='nesw')
        MB3.grid(column=0,row=4,sticky='nesw')
        MB4.grid(column=0,row=5,sticky='nesw')
        MB5.grid(column=0,row=6,sticky='nesw')
        Sidebar.grid(column=0,row=0)
    def start(win): #Runs at end of Mwin startup, initializes all menu imgs under menu window.
        #print('Loading images ','-cSM line 108')
        '''menuImg0 = PhotoImage(file='Images/sidebar/Menu.png')
        menuImg1 = PhotoImage(file='Images/sidebar/Translation.png')
        menuImg2 = PhotoImage(file='Images/sidebar/Numbers.png')
        menuImg3 = PhotoImage(file='Images/sidebar/Pronunciation Placeholder.png')
        menuImg4 = PhotoImage(file='Images/sidebar/Settings.png')
        menuImg5 = PhotoImage(file='Images/sidebar/Credits.png')'''
        menuImg0 = ImageTk.PhotoImage(iT.preformTint('Images/sidebar/Menu.png',str(Theme[7])))
        menuImg1 = ImageTk.PhotoImage(iT.preformTint('Images/sidebar/Translation.png',str(Theme[7])))
        menuImg2 = ImageTk.PhotoImage(iT.preformTint('Images/sidebar/Numbers.png',str(Theme[7])))
        menuImg3 = ImageTk.PhotoImage(iT.preformTint('Images/sidebar/Pronunciation.png',str(Theme[7]))) #Pronunciation Placeholder.png or Icon Pronunciation.png also avaliable
        menuImg4 = ImageTk.PhotoImage(iT.preformTint('Images/sidebar/Settings.png',str(Theme[7])))
        menuImg5 = ImageTk.PhotoImage(iT.preformTint('Images/sidebar/Credits.png',str(Theme[7])))

        #MenuImgs.clear()
        SidebarMenu.MenuImgs.append(menuImg0)
        SidebarMenu.MenuImgs.append(menuImg1)
        SidebarMenu.MenuImgs.append(menuImg2)
        SidebarMenu.MenuImgs.append(menuImg3)
        SidebarMenu.MenuImgs.append(menuImg4)
        SidebarMenu.MenuImgs.append(menuImg5)

def createFontTranslationWin(): #This function contains all of the tkinter widgets and functions nececary to be defined before them in order to create the font translation window. Relevent support files: iT,GRC,random.md
    #Window Register Management
    if CheckWindowRegister('T') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Twin = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(Twin,'T') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Twin.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(Twin,WinCode,'T')) #Use saved code to remove from register
    Twin.title("Avalian Font Translation")
    Twin.configure(background=Theme[2])
    #End Window management

    EcoverStatus = True
    TcoverStatus = True
    StringVar1 = ''
    RefranceImg = ImageTk.PhotoImage(iT.preformTint("Images/CharRefPlaceholderTransAdjCropResize61.png",str(Theme[2])))
    def switchCover(inp): # Swiches the visibility of the centeral elements of this page to allow for practice of translation with or without the key or the direct translation. Does this by switching the background of the transparent image key and English text display respectivly to the same color as their foreground color.
        nonlocal EcoverStatus    
        nonlocal TcoverStatus    
        if inp == 1:
            if EcoverStatus == True:
                English.config(fg=Theme[1])
                switch1.config(relief=RAISED)
                EcoverStatus = False
            else:
                English.config(fg=Theme[0])
                switch1.config(relief=SUNKEN)
                EcoverStatus = True
        elif inp == 2:
            if TcoverStatus == True:
                refimg.config(bg=Theme[0])
                switch2.config(relief=RAISED)
                TcoverStatus = False
            else:
                refimg.config(bg=Theme[2])
                switch2.config(relief=SUNKEN)
                TcoverStatus = True
    def chunk_string(string, maxsize):
            #return [string[i:i + maxsize] for i in range(0, len(string), maxsize)]
        global StringVar1
        car = int(len(string))
        k = maxsize
        for i in range(car):
            #print("k: ",k," = ",string[i])
            #for k in range(maxsize):
            if k == 0:
                if string[i] == " ":
                    StringVar1 += "/n"
                    k = maxsize
                else:
                    StringVar1 += string[i]
            else:
                StringVar1 += string[i]
                k-=1
    def changeText(inp): #handles changing the English and scratch text displays from the user input buttons. In all cases except the custom input button being pressed the function calls ChallengeRandSample(arg) from GatherRandomCharacters.py with the index of the button as the argument the result of this function is saved to Ntext. Otherwise if the index is 22 or Custom Input the function grabs the text in the custom input text box and saves it to Ntext. Next Ntext is tested if it is > 40 characters. If it is the text is chunked to fit as well as possible into that space by each word. This is done by seeking forward until the maxsize (40) is reached and then searching for the next space and inserting a newline character. This method prevents code from breaking ig the user inputs a word greater that 40 chars. Finaly this edited string is sent to update English and Scratch labels.  
        global StringVar1
        global Ftext
        maxsize = 40
        Ftext = ''
        if inp == 0:
            Ntext = GRC.ChallengeRandSample(0)
            #pronounciationDisp(Ntext)
        elif inp == 1:
            Ntext = GRC.ChallengeRandSample(1)
            #pronounciationDisp(Ntext)
        elif inp == 2:
            Ntext = GRC.ChallengeRandSample(2)
            #pronounciationDisp(Ntext)
        elif inp == 3:
            Ntext = GRC.ChallengeRandSample(3)
        elif inp == 4:
            Ntext = GRC.ChallengeRandSample(4)
        elif inp == 22:
            Ntext = cInput.get("1.0", "end-1c")
        
        if len(Ntext) > 40:
            #StringVar1 = chunk_string(Ntext, maxsize)
            Ftext = ""
            car = int(len(Ntext))
            k = maxsize
            for i in range(car):
                #print("k: ",k," = ",Ntext[i]) #DEBUG
                #for k in range(maxsize):
                if k == 0:
                    if Ntext[i] == " ":
                        Ftext += "\n"
                        k = maxsize
                    else:
                        Ftext += Ntext[i]
                else:
                    Ftext += Ntext[i]
                    k-=1
            
            Scratch.config(text=Ftext)
            English.config(text=Ftext)     
        else:
            Ftext +=str(Ntext)
            #print('Ftex',Ftext) #DEBUG
            #StringVar1 = Ftext
            #print('Str1',StringVar1) #DEBUG w
            Scratch.config(text=Ftext)
            English.config(text=Ftext)
    
    border_frame = Frame(Twin,background=Theme[2],borderwidth="4px")
    content_frame = Frame(border_frame, background=Theme[0],borderwidth= "12px")
    
    SidebarMenu(Twin,border_frame) #Create Menu Sidebar    

    #scrollbar = Scrollbar(content_frame, orient="vertical", command=content_frame.yview)
    #https://www.tutorialspoint.com/implementing-a-scrollbar-using-grid-manager-on-a-tkinter-window
    Scratch = Label(content_frame,text=StringVar1,font=('avali scratch',30), background="white", borderwidth="10px", foreground=Theme[2])
    English = Label(content_frame,text=StringVar1,font=('arial',20),bg=Theme[0],fg=Theme[0]) #25 pt lines up with scratch, 20 fits nicely and is about the same size. 
    buttonFrame = Frame(content_frame,background=Theme[0])
    swichFrame = Frame(content_frame)
    switch1 = Button(swichFrame,text="Hide English",command=lambda: switchCover(1),relief=SUNKEN,bg=Theme[8],fg=Theme[9])
    switch2 = Button(swichFrame,text="Hide Table",command=lambda: switchCover(2),relief=SUNKEN,bg=Theme[8],fg=Theme[9])
    Option0 = Button(buttonFrame,text="4 letter word",command=lambda: changeText(0),bg=Theme[8],fg=Theme[9])
    Option1 = Button(buttonFrame,text="6 letter Word",command=lambda: changeText(1),bg=Theme[8],fg=Theme[9])
    Option2 = Button(buttonFrame,text="Sentence",command=lambda: changeText(2),bg=Theme[8],fg=Theme[9])
    Option3 = Button(buttonFrame,text="Paragraph",command=lambda: changeText(3),bg=Theme[8],fg=Theme[9])
    Option4 = Button(buttonFrame,text="Number",command=lambda: changeText(4),bg=Theme[8],fg=Theme[9])
    Option22 = Button(buttonFrame,text="Custom Input",command=lambda: changeText(22),bg=Theme[8],fg=Theme[9])
    cInput = Text(content_frame, height = 3, width = 71,background=Theme[6])
    cInput.bind("<Return>",lambda event: changeText(22))
    refimg = Label(content_frame,image=RefranceImg,width=895,height=61,background=Theme[2])
    #content_frame.bind("<Configure>", lambda e: content_frame.configure(scrollregion=content_frame.bbox("all")))
    #drawing

    border_frame.pack()
    content_frame.grid(row=0,column=1)

    English.grid(column=0,row=2,columnspan=8)
    Scratch.grid(column=0,row=3,columnspan=8)
    swichFrame.grid(column=7,row=2)
    buttonFrame.grid(column=0,row=0,columnspan=8)
    BpaddingX = 20
    switch1.grid(column=0,row=0) #,pady=5))
    switch2.grid(column=0,row=1)
    Option0.grid(column=1,row=0,padx=BpaddingX)
    Option1.grid(column=2,row=0,padx=BpaddingX)
    Option2.grid(column=3,row=0,padx=BpaddingX)
    Option3.grid(column=4,row=0,padx=BpaddingX)
    Option4.grid(column=5,row=0,padx=BpaddingX)
    Option22.grid(column=0,row=0,padx=BpaddingX)
    cInput.grid(column=0,row=1, columnspan=8)
    refimg.grid(column=0,row=4,columnspan=8)
    #cover.grid(column=0,row=0)
    Twin.mainloop()
    
def createCreditsWin(): #This function contains all of the tkinter widgets and functions nececary to be defined before them in order to create the credits window. Relevent support files: None
    #Window Register Management
    if CheckWindowRegister('C') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Cwin = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(Cwin,'C') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Cwin.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(Cwin,WinCode,'C')) #Use saved code to remove from register
    Cwin.title("Avalian Translation Credits")
    Cwin.configure(background=Theme[2])

    #End Window management

    border_frame = Frame(Cwin,background=Theme[2],borderwidth="4px")
    content_frame = Frame(border_frame, background=Theme[0],borderwidth= "12px")
    Preamble = Label(content_frame,text="I hope some birbs can find some fun or use in this.\nYou can contact me reguarding this software via\n\
Telegram @RenauliSnow.\n\nA deep thanks goes to everyone in this community for\n\
perpetuating this amazing species. For their specific\n\
contributions to this project thank you to the following:\n",justify='left',font=('arial',16),background=Theme[0],foreground=Theme[1]) 
    #insert line break
    Credit = Label(content_frame,text="Programed by Renauli Snow(Ralsdoge) for the community.\nVersion 1 in development from 11/23/2024 to 7/13/2025.",font=('arial',16),background=Theme[0],foreground=Theme[1])
    Credits = Label(content_frame,text=" • Cutesune (RyuujinZero) for creating the Avali Species\n \
• Avali A Comprehensive Guide: Todd Avali\n \
• Scratch Font: Icebelly and Someguynameddavid\n \
• Avali Number System: Ceital Tesai\n \
• Avali hd icon: tikitree2\n\n\
For presenting me the joys of this community:\n \
• FelisRandomis\n \
• RitualNeo\n \
• Randomking1423\n \
• And many, many others. \
",font=('arial',16),justify='left',background=Theme[0],foreground=Theme[1]) 
    License = Label(content_frame,text="\nThis project is licensed under the GNU General Public License v3 (GPLv3).",font=('arial',14),background=Theme[0],foreground=Theme[1])
    
    #Scratch = Label(content_frame,text="test",font=('avali scratch',30), background="white", borderwidth="10px", foreground="#fc850f")
    #English = Label(content_frame,text="test",font=('arial',20),bg='black') #25 pt lines up with scratch, 20 fits nicely and is about the same size. 
    
    border_frame.pack()
    content_frame.pack()
    Credit.grid(column=0,row=0)
    Preamble.grid(column=0,row=1)
    Credits.grid(column=0,row=2)
    License.grid(column=0,row=3)
    '''Credit1.grid(column=0,row=3)
    Credit2.grid(column=3,row=4)
    Credit3.grid(column=0,row=5)
    Credit3.grid(column=0,row=6)
    Credit4.grid(column=0,row=7)'''
    #.grid(column=0,row=4)
    Cwin.mainloop()

def createOptionsWin(): #This function contains all of the tkinter widgets and functions nececary to be defined before them in order to create the font translation window. Relevent support files: settings.ini,
    #Window Register Management
    if CheckWindowRegister('O') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Owin = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(Owin,'O') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Owin.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(Owin,WinCode,'O')) #Use saved code to remove from register
    Owin.title("Avalian Translation Options")
    Owin.configure(background=Theme[2])

    #End Window management

    def button(setting,state): #accepts button commands and textboxes for options
        print("runing",'-cOW->b line 369')
        if setting == 0:
            if state == 1:
                input = TextBox.get("1.0",END)
                if input == '' or input == ' ':
                    return(False)
                else:
                    try:
                        input = int(input)
                    except:
                        GO.errorMsg("Error: Non Integer Input","Theme input is restricted to integer values. To create a custom theme open settings.ini and input hex color codes acordingly observing the presets. Note the position of your them and input it in options.")
                        return(False)
                curTheme = GO.readIni("Theme","setTheme")
                Bottom = GO.readIni("Pronunciation","Hpron")
                #print("Theme:",int(curTheme[1])+input,"versus, Bottom:",Bottom[1]-1)
                if (int(curTheme[1])+input) < (Bottom[1]-1):
                    #print("valid")
                    GO.writeIni("Theme","setTheme",str(input))
                    GO.infoMsg('Success','Your theme has been updated, please restart the aplication!')
                else: 
                    GO.infoMsg('Failure','Your theme has NOT been updated, your input is out of the possible selctions for themes.')
                    #print("Not")
                #if GO.retrieveTheme(Theme[0],Theme[1],1):

        if setting == 1:
            #if LSButton2.cget('relief') == FLAT:
            if state == 1:
                #print("Right")
                LSButton2.config(relief=RAISED,bg=Theme[2],activebackground=Theme[2],state=NORMAL)
                RSButton2.config(relief=FLAT,bg='lightgrey',activebackground='lightgrey',state=DISABLED)#or FLAT
            else:
                #print("Left")
                LSButton2.config(relief=FLAT,bg='lightgrey',activebackground='lightgrey',state=DISABLED)#or FLAT
                RSButton2.config(relief=RAISED,bg=Theme[2],activebackground=Theme[2],state=NORMAL)
    def setbuttons(p): #sets all buttons acording to settings in settings.ini
        O1 = GO.readIni("Theme","setTheme")
        O2 = GO.readIni("Theme","setTheme")
        O3 = GO.readIni("Pronunciation","Hpron")
        O4 = GO.readIni("Pronunciation","Cchars")
        
        
        TextBox.insert("1.0", "This is some text to insert") 
        TextBox.insert("1.0", str(O1)) 
    
    #Creating Objects:
    border_frame = Frame(Owin,background=Theme[2],borderwidth="4px")
    content_frame = Frame(border_frame, background=Theme[0],borderwidth= "12px")
    
    SidebarMenu(Owin,border_frame) #Wow this worked in its first aplication imedietly with no bug fixing whatsoeverthisisdefinitlyatrap.
 
    Title = Label(content_frame,text="Options",font=('arial',20),background=Theme[0],foreground=Theme[1]) 
    
    Setting1 = Frame(content_frame,background=Theme[0])
    Title1 = Label(Setting1,text="Dark, Light, & Custom Themes",font=('arial',16),background=Theme[0],foreground=Theme[1]) 
    Desc1 = Label(Setting1,text="Change the theme of the app. Enter 1 for Light and 2\nfor Dark. Make your own custom themes in 'settings.ini'.",font=('arial',10),background=Theme[0],foreground=Theme[1]) 
    toggleSwitch1 = Frame(Setting1,highlightbackground=Theme[1],highlightthickness=3)
    TextBox = Text(toggleSwitch1,bg=Theme[6],font=("Arial",16),width=1,height=1)#Activebackground=Theme[2]
    TextBox.bind("<Return>",lambda event: button(0,1))
    RSButton1 = Button(toggleSwitch1,relief=RAISED,bg=Theme[2],activebackground=Theme[2],text='Submit',command=lambda: button(0,1))
    

    Setting5 = Frame(content_frame,background=Theme[0])
    Title5 = Label(Setting5,text="New Window Open Option        ",font=('arial',16),background=Theme[0],foreground=Theme[1]) 
    Desc5 = Label(Setting5,text="Sets if new windows are managed (only one of each type\nopen at a time) or unmanaged (Open as many as you\nwould like at once).",font=('arial',10),background=Theme[0],foreground=Theme[1]) 
    toggleSwitch5 = Frame(Setting5,highlightbackground=Theme[1],highlightthickness=3)
    LSButton5 = Button(toggleSwitch5,relief=FLAT,bg=Theme[6],activebackground=Theme[6],text='   ',command=lambda: button(4,0))#Activebackground=Theme[2]
    RSButton5 = Button(toggleSwitch5,relief=RAISED,bg=Theme[2],activebackground=Theme[2],text='   ',command=lambda: button(4,1))

    Setting2 = Frame(content_frame,background=Theme[0])
    Title2 = Label(Setting2,text="Number Canvas Orientation     ",font=('arial',16),background=Theme[0],foreground=Theme[1]) 
    Desc2 = Label(Setting2,text="Sets if Number Camvas is set horizontaly or verticaly\nby default on opening.",font=('arial',10),background=Theme[0],foreground=Theme[1]) 
    toggleSwitch2 = Frame(Setting2,highlightbackground=Theme[1],highlightthickness=3)
    LSButton2 = Button(toggleSwitch2,relief=FLAT,bg=Theme[6],activebackground=Theme[6],text='   ',command=lambda: button(1,0))#Activebackground=Theme[2]
    RSButton2 = Button(toggleSwitch2,relief=RAISED,bg=Theme[2],activebackground=Theme[2],text='   ',command=lambda: button(1,1))
    
    Setting3 = Frame(content_frame,background=Theme[0])
    Title3 = Label(Setting3,text="Pronunciation Clamping Chars. ",font=('arial',16),background=Theme[0],foreground=Theme[1]) 
    Desc3 = Label(Setting3,text="Sets your default selction for the Pronuciation\nclamping characters. i.e. [] or ()",font=('arial',10),background=Theme[0],foreground=Theme[1]) 
    toggleSwitch3 = Frame(Setting3,highlightbackground=Theme[1],highlightthickness=3)
    LSButton3 = Button(toggleSwitch3,relief=FLAT,bg=Theme[6],activebackground=Theme[6],text='   ',command=lambda: button(2,0))#Activebackground=Theme[2]
    RSButton3 = Button(toggleSwitch3,relief=RAISED,bg=Theme[2],activebackground=Theme[2],text='   ',command=lambda: button(2,1))
    
    Setting4 = Frame(content_frame,background=Theme[0])
    Title4 = Label(Setting4,text="N Pronuciation Replacement Chars.",font=('arial',16),background=Theme[0],foreground=Theme[1]) 
    Desc4 = Label(Setting4,text='Sets your default selction for the Pronuciation\nof the letter "n". i.e. a short pause or "hthk".',font=('arial',10),background=Theme[0],foreground=Theme[1]) 
    toggleSwitch4 = Frame(Setting4,highlightbackground=Theme[1],highlightthickness=3)
    LSButton4 = Button(toggleSwitch4,relief=FLAT,bg=Theme[6],activebackground=Theme[6],text='   ',command=lambda: button(3,0))#Activebackground=Theme[2]
    RSButton4 = Button(toggleSwitch4,relief=RAISED,bg=Theme[2],activebackground=Theme[2],text='   ',command=lambda: button(3,1))
    
    #Griding Objects
    border_frame.pack()
    content_frame.grid(column=1,row=0)
    Title.grid(column=0,row=0)
    #Preamble.grid(column=0,row=0)
    ###Option 1
    Title1.grid(column=0,row=0)
    Desc1.grid(column=0,row=1,columnspan=2)
    TextBox.grid(column=0,row=0,sticky='nesw')
    RSButton1.grid(column=1,row=0)
    toggleSwitch1.grid(column=3 ,row=0)

    ###Option 5
    Title5.grid(column=0,row=0)
    Desc5.grid(column=0,row=1,columnspan=2)
    LSButton5.grid(column=0,row=0)
    RSButton5.grid(column=1,row=0)
    toggleSwitch5.grid(column=3 ,row=0)

    ###Option 2
    Title2.grid(column=0,row=0)
    Desc2.grid(column=0,row=1,columnspan=2)
    LSButton2.grid(column=0,row=0)
    RSButton2.grid(column=1,row=0)
    toggleSwitch2.grid(column=3 ,row=0)
    
    ###Option 3
    Title3.grid(column=0,row=0)
    Desc3.grid(column=0,row=1,columnspan=2)
    LSButton3.grid(column=0,row=0)
    RSButton3.grid(column=1,row=0)
    toggleSwitch3.grid(column=3 ,row=0)

    ###Option 4
    Title4.grid(column=0,row=0)
    Desc4.grid(column=0,row=1,columnspan=2)
    LSButton4.grid(column=0,row=0)
    RSButton4.grid(column=1,row=0)
    toggleSwitch4.grid(column=3 ,row=0)

    Setting1.grid(column=0,row=1)
    Setting2.grid(column=0,row=2)
    Setting5.grid(column=0,row=3)
    Setting3.grid(column=0,row=4)
    Setting4.grid(column=0,row=5)

    NotComplete1 = Label(content_frame,text="Coming Soon",font=('arial',25),background=Theme[0],foreground=Theme[1]) 
    NotComplete2 = Label(content_frame,text="Coming Soon",font=('arial',25),background=Theme[0],foreground=Theme[1]) 
    NotComplete3 = Label(content_frame,text="Coming Soon",font=('arial',25),background=Theme[0],foreground=Theme[1]) 
    NotComplete4 = Label(content_frame,text="Coming Soon",font=('arial',25),background=Theme[0],foreground=Theme[1]) 

    NotComplete1.grid(column=0,row=2)
    NotComplete2.grid(column=0,row=3)
    NotComplete3.grid(column=0,row=4)
    NotComplete4.grid(column=0,row=5)

    Owin.mainloop()

def createNumbersWin():
    #Window Register Management
    if CheckWindowRegister('N') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Nwin = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(Nwin,'N') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Nwin.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(Nwin,WinCode,'N')) #Use saved code to remove from register
    Nwin.configure(background=Theme[2])
    #End Window management
    
    Inscriptions = []
    LoadedInscriptions = []
    B10NUM = str(0)
    B12NUM = str(0)
    VERT = 0
    NEG = 0
    b10Cover = 0
    b12Cover = 0
    #testimg = ImageTk.PhotoImage(Image.open("numChars/Anum1-6.png"))
    
    border_frame = Frame(Nwin,background=Theme[2],borderwidth="4px")
    content_frame = Frame(border_frame, background=Theme[0],borderwidth= "12px")
    
    #Load settings
    HV = GO.readIni("Numbers","HV") #read the options
    if HV == 0 or HV == 1: #if valid entry set the orientation of canvas
        if HV == 0: #Horizontal 
            panel = Canvas(content_frame, bg=Theme[0], width=800, height=100)
            panel.grid(column=0,row=5,columnspan=5,rowspan=1) #Wide mode
        if HV == 1: #Vertical
            panel = Canvas(content_frame,bg=Theme[0], width=100, height=600)
            panel.grid(column=0,row=0,columnspan=1,rowspan=5) #long mode
            VERT = 1
    else: #else defult horizontal;
        panel = Canvas(content_frame,bg=Theme[0], width=800, height=100)
        panel.grid(column=0,row=5,columnspan=5,rowspan=1) #Wide mode 

    class spawnImg():
        def __init__(self,filepath):
            self.name = filepath
            self.image = Image.open(filepath)
            self.photo = ImageTk.PhotoImage(self.image)
            LoadedInscriptions.append(self)

        def read(self):
            return self.name
        
        def present(self):
            return self.photo
        
        def getDimensions(self):
            height = self.photo.height()
            width = self.photo.width()
            return (width,height)

    def checkLoad(filepath): #check if image has already been loaded
        for i in range(len(LoadedInscriptions)-1):
            if filepath == LoadedInscriptions[i].read():
                print('Already loaded!','-cNW->cL line 533')
                return i
        #print('Loading '+str(filepath)+'...',end='  ')
        spawnImg(filepath)
        #print('Loaded!')
        #print(len(LoadedInscriptions)-1,'===',LoadedInscriptions[len(LoadedInscriptions)-1])
        return len(LoadedInscriptions)-1

    def writeImg(x,y,filepath): #put image on canvas
        loadedIndex = checkLoad(filepath)
        panel.create_image(x, y, image=LoadedInscriptions[loadedIndex].present(),anchor="nw")
        return loadedIndex
    
    def get_image_dimensions(patht):
        try:
            with Image.open(str(patht)) as img:
                return img.width, img.height
        except Exception as e:
            print(f"Error: {e}")
            return None


    def writeNumber(x,y,manifest,vert): #write full number to canvas
        #add vertical option
        panel.delete('all') #avoid memory leak
        #Horizintal
        lastWidth = 0
        lastHeight = 0
        lastX = 0
        lastY = 0
        centerlineH = 92 #maxHeight of tallest img in set
        centerlineV = 60 #maxWidth of widest img in set
        if vert == 0: #Horizontal
            for i in range(len(manifest)):
                if i == 0:
                    lastWidth,lastHeight = get_image_dimensions('Images/numChars/'+str(manifest[0])+'.png')
                    y = centerlineH/2 -lastHeight/2
                    lastX,lastY = x,y
                    Index = writeImg(x,y,'Images/numChars/'+str(manifest[0])+'.png')
                    #print(x,y,end=',')
                    #print(lastWidth,lastHeight)
                    
                else:
                    newX = lastX+lastWidth+10
                    lastWidth,lastHeight = get_image_dimensions('Images/numChars/'+str(manifest[i])+'.png')
                    newY = centerlineH/2 - lastHeight/2
                    lastX,lastY = newX,newY
                    Index = writeImg(newX,newY,'Images/numChars/'+str(manifest[i])+'.png')
                    #print(newX,newY,end=',')
                    #print(lastWidth,lastHeight)
                #insert Inbetween Characters
                if manifest[i] == 'Decimal' or i == len(manifest)-1: #if last character was a decimal dont put an in-between glyph OR if last glyph in the nnumber
                    pass
                else:
                    newX = lastX+lastWidth/2
                    newY = centerlineH/2
                    Index = writeImg(newX,newY,'Images/numChars/InbetweenHori.png')
                    #print('Inbetween:',newX,newY,end=',')
                    #print(LoadedInscriptions[Index].getDimensions())
        else:
            if i == 0:
                Index = writeImg(x,y,'Images/numChars/'+str(manifest[0])+'.png')
                lastWidth,lastHeight = LoadedInscriptions[Index].getDimensions()
                lastX,lastY = x,y
                #print(lastWidth,lastHeight)
                
            else:
                newX = lastX
                newY = lastY+lastHeight+10
                Index = writeImg(newX,newY,'Images/numChars/'+str(manifest[i])+'.png')
                lastWidth,lastHeight = LoadedInscriptions[Index].getDimensions()
                lastX,lastY = newX,newY
                #print(newX,newY)
                #print(lastWidth,lastHeight)
    
    def newNumber(b10Num):
        nonlocal VERT
        nonlocal B10NUM
        nonlocal B12NUM
        Negitivenum = 0
        if b10Num < 0:
            Negitivenum = 1
            B10NUM = -b10Num #+ (-b10Num*2)
        else:
            B10NUM = b10Num
        b10EnglishDisp.config(text=b10Num)
        #print('b10Num:',b10Num)
        #print('B10NUM:',B10NUM)
        B12NUM = AN.base12numberConvert(B10NUM)
        b12num = B12NUM
        if Negitivenum == 1:
            B12NUM.insert(0,'Negitive')
        #print('B12NUM:',B12NUM,'-cNW->nN line 604')
        b12num = str(b12num).replace(" ","").replace("'","").replace("Negitive",'-').replace(",","").replace("[","").replace("]","")
        #b12num = str(b12num).replace("'Negitive', ","").replace(", ","").replace("]","") #Does not always work in cases of A B or other uniqe
        #print('b12num:',b12num,'-cNW->nN line 604')

        b12EnglishDisp.config(text=b12num)        
        manifest = AN.base12ImageRef(B10NUM,B12NUM,Negitivenum) 
        #print('manifest:',manifest)
        
        writeNumber(2,2,manifest,VERT)   
    
    def buttonDecode(i):
        nonlocal VERT
        nonlocal NEG
        nonlocal b10Cover
        nonlocal b12Cover
        if i == 0:
            userIn = userInput.get("1.0",END)
            #print(userIn)
            userIn = int(userIn)
            #print(type(userIn))
            #validate
            #print('VERT: ',VERT)
            newNumber(userIn)

            #print('Done!')
        elif i == 1:
            #do random
            #print('Do random!')
            randomNum = random.randint(int(MinSize.get()),int(MaxSize.get()))
            decLength = int(DecimalLength.get())-1
            #print(int(DecimalLength.get()),'-->',int(DecimalLength.get())-1)
            if decLength != -1:
                decimalInt = random.randint(10**decLength,(10**(decLength+1))-1)
                #print('Decimal:',decimalInt)
                decimalComponent = str(decimalInt*0.1**(decLength+1))
                #print('Decimal:',decimalComponent)
                decimalComponent = decimalComponent.split()
                #print('Decimal:',decimalComponent)
                for i in range(len(decimalComponent)):
                    total = len(str(decLength))+2
                    if i+1 < total:
                        pass
                    else:
                        pass
                        #print(decimalComponent)
                        
                #randomNum = randomNum+decimalComponent
                #print(randomNum)
                #Add negitive sign if applicable
                if NEG == 1: #add -
                    randomNum = randomNum-(randomNum*2)
                    #print(randomNum,'negitive:',randomNum)
                elif NEG == 2:
                    if random.randint(1,100) >= 46: #45/55 negitve/positive
                        #add -
                        randomNum = randomNum-(randomNum*2)
                        #print(randomNum,'negitive:',randomNum)
                else:
                    pass
                newNumber(randomNum)
            else:
                pass
                
            
        elif i == 2: #vertical or horizontal
            #print('VERT IN:',VERT)
            if VERT == 0:
                VERT = 1
                panel.config(height=600,width=100) #long mode
                panel.grid(column=0,row=0,columnspan=1,rowspan=5)
            else: 
                VERT = 0
                panel.config(height=100,width=800) #Wide mode
                panel.grid(column=0,row=5,columnspan=5,rowspan=1)
            #print('VERT OUT:',VERT)
            #GO.writeIni("Numbers","HV",VERT) #write prefrence back to ini file
        
        elif i == 3: #Random Number Negitive chance
            if NEG == 2: #Negitive and positive
                NEG = 0
                NegitiveState.config(text='Positive')
            elif NEG == 0:
                NEG = 1
                NegitiveState.config(text='Negitive')
            elif NEG == 1:
                NEG = 2
                NegitiveState.config(text='Neg & Pos')
        elif i == 4: #Hide unhide displays
            if b10Cover == 0:
                b10Cover = 1
                b10EnglishDisp.config(background=Theme[1])
                b10EnglishDispButton.config(text='Unhide')
            else:
                b10Cover = 0
                b10EnglishDisp.config(background=Theme[0])
                b10EnglishDispButton.config(text='Hide')
        elif i == 5: #Hide unhide displays
            if b12Cover == 0:
                b12Cover = 1
                b12EnglishDisp.config(background=Theme[1])
                b12EnglishDispButton.config(text='Unhide')
            else:
                b12Cover = 0
                b12EnglishDisp.config(background=Theme[0])
                b12EnglishDispButton.config(text='Hide')
    
    #Create Menu Sidebar    
    SidebarMenu(Nwin,border_frame)

    util_frame = Frame(content_frame, background=Theme[0],borderwidth= '12px')
    random_frame = Frame(content_frame, background=Theme[0],borderwidth= '12px')
    ###Title + Support
    Title = Label(content_frame,text='Avalian Base 12 System',font=('arial',18),background=Theme[0],foreground=Theme[1])
    
    ###Random Interface
    RandLabel = Label(random_frame,text='Random Num. Gen.',font=('arial',14),background=Theme[0],foreground=Theme[1])
    MaxSize = Scale(random_frame, from_=0, to=1000,orient = "horizontal",fg=Theme[1],bg=Theme[0]) #Slider 
    MinSize = Scale(random_frame, from_=0, to=1000,orient = "horizontal",fg=Theme[1],bg=Theme[0]) #Slider
    DecimalLength = Scale(random_frame, from_=0, to=10,orient = "horizontal",fg=Theme[1],bg=Theme[0]) #Slider
    DecimalLengthLabel = Label(random_frame,text="Decimal Length",font=('arial',10),background=Theme[0],foreground=Theme[1])
    DecimalLengthWarning = Label(random_frame,text="(Not added yet, confused\non how it'd work)",font=('arial',10),background=Theme[0],foreground=Theme[1])
    MaxSizeLabel = Label(random_frame,text='Max Size',font=('arial',10),background=Theme[0],foreground=Theme[1])
    MinSizeLabel = Label(random_frame,text='Min Size',font=('arial',10),background=Theme[0],foreground=Theme[1])
    MaxSize.set(125)
    MinSize.set(20)
    DecimalLength.set(1)
    NegitiveState = Button(random_frame,text='Positive',command=lambda:buttonDecode(3),bg=Theme[8],fg=Theme[9]) #wether to generate negitive numbers or not
    randomNumGo = Button(random_frame,text='Submit',command=lambda:buttonDecode(1),bg=Theme[8],fg=Theme[9]) #submit random num
    def enterHandler():
        buttonDecode(0)
        return "break"
    ###Options###
    userInput = Text(util_frame,width=30,height=1,bg=Theme[6]) #User in Textbox
    userInput.bind("<Return>",lambda event: enterHandler())

    userInGo = Button(util_frame,text='Submit',command=lambda:buttonDecode(0),bg=Theme[8],fg=Theme[9]) #submit user input from Userinput (Valideate)
    base10Label = Label(util_frame,text='Base-10:',font=('arial',10),background=Theme[0],foreground=Theme[1])
    base12Label = Label(util_frame,text='Base-12:',font=('arial',10),background=Theme[0],foreground=Theme[1])
    b12EnglishDisp = Label(util_frame,text=B12NUM[0],font=('arial',12), background=Theme[0], foreground=Theme[1]) #Base12 number display in english
    b10EnglishDisp = Label(util_frame,text=B10NUM,font=('arial',12), background=Theme[0], foreground=Theme[1]) #Base10 number display in english
    b10EnglishDispButton = Button(util_frame,text='Hide',command=lambda:buttonDecode(4),bg=Theme[8],fg=Theme[9]) 
    b12EnglishDispButton = Button(util_frame,text='Hide',command=lambda:buttonDecode(5),bg=Theme[8],fg=Theme[9]) 
    HVButton = Button(util_frame,text='Horizontal/Vertical',command=lambda:buttonDecode(2),bg=Theme[8],fg=Theme[9])#Horizontal Vertical numbering toggle
    HVdescription = Label(util_frame,text="Swich between formal vertical structure and casual horizontal dispaly.",background=Theme[0],foreground=Theme[1]) 
    ###

    
    border_frame.pack()
    content_frame.grid(column=1,row=0)

    Title.grid(column=1,row=0,columnspan=3)
    util_frame.grid(column=1,row=1,columnspan=3,rowspan=3,sticky='nesw')
    HVButton.grid(column=1,row=0)
    HVdescription.grid(column=0,row=1,columnspan=3,)
    userInput.grid(column=0,row=2,columnspan=2,sticky='e')
    userInGo.grid(column=2,row=2,columnspan=1)
    base10Label.grid(column=0,row=4)
    base12Label.grid(column=0,row=5)
    b10EnglishDisp.grid(column=1,row=4,columnspan=2)
    b12EnglishDisp.grid(column=1,row=5,columnspan=2)
    b10EnglishDispButton.grid(column=2,row=4,columnspan=1)
    b12EnglishDispButton.grid(column=2,row=5,columnspan=1)
    #Random
    random_frame.grid(column=4,row=0,columnspan=2,rowspan=3,sticky='wns')
    RandLabel.grid(column=0,row=0,columnspan=3)
    MaxSize.grid(column=1,row=2,columnspan=2)
    MinSize.grid(column=1,row=4,columnspan=2)
    DecimalLength.grid(column=1,row=6,columnspan=2)
    MaxSizeLabel.grid(column=0,row=1,columnspan=2)
    MinSizeLabel.grid(column=0,row=3,columnspan=2)
    DecimalLengthLabel.grid(column=0,row=5,columnspan=2)
    DecimalLengthWarning.grid(column=0,row=6,columnspan=2)
    NegitiveState.grid(column=0,row=7,columnspan=2)
    randomNumGo.grid(column=2,row=7)
    
    Nwin.mainloop()

def createPronunciationWin():
    #Window Register Management
    if CheckWindowRegister('P') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Pwin = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(Pwin,'P') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Pwin.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(Pwin,WinCode,'P')) #Use saved code to remove from register
    Pwin.title("Avalian Pronunciation")    
    Pwin.configure(background=Theme[2])
    #End Window management
    StringVar1 = ''
    StringVar2 = ''
    Ntext = ''
    ###Functions
    def changeText(inp):
        global StringVar1
        global StringVar2
        maxsize = 70
        Ftext = ''
        if inp == 0:
            Ntext = GRC.ChallengeRandSample(0)
        elif inp == 1:
            Ntext = GRC.ChallengeRandSample(1)
        elif inp == 2:
            Ntext = GRC.ChallengeRandSample(2)
        elif inp == 3:
            Ntext = GRC.ChallengeRandSample(3)
        elif inp == 4:
            Ntext = GRC.ChallengeRandSample(4)
        elif inp == 22:
            Ntext = cInput.get("1.0", "end-1c")
        StringVar1 = Ntext
        StringVar2 = str(AP.pronounciationDisp(Ntext,Hdropclicked.get(),ClampingCharsSelected.get()))
        
        #print('strvar2:',StringVar2)
        #print('str(strvar2):',str(StringVar2))
        if len(Ntext) > maxsize:
            Ftext = ""
            car = int(len(Ntext))
            k = maxsize
            for i in range(car):
                if k == 0:
                    if Ntext[i] == " ":
                        Ftext += "\n"
                        k = maxsize
                    else:
                        Ftext += Ntext[i]
                else:
                    Ftext += Ntext[i]
                    k-=1
            English.config(text=Ftext)
            StringVar1=Ftext     

            Ftext = ""
            car = int(len(StringVar2))
            k = maxsize
            for i in range(car):
                if k == 0:
                    if StringVar2[i] == " ":
                        Ftext += "\n"
                        k = maxsize
                    else:
                        Ftext += StringVar2[i]
                else:
                    Ftext += StringVar2[i]
                    k-=1
            EnglishO.config(text=Ftext)
            StringVar2=Ftext     
        else:
            English.config(text=Ntext)
            EnglishO.config(text=StringVar2)

    border_frame = Frame(Pwin,borderwidth="4px",background=Theme[2])#background="#fc850f"
    content_frame = Frame(border_frame,borderwidth= "12px",background=Theme[0])
    
    SidebarMenu(Pwin,border_frame)

    ###Labels
    PronunciationTableHead = Label(content_frame,text='Unpronounceable Characters',font=('arial',20), background=Theme[0], foreground=Theme[1])
    PronunciationDesc = Label(content_frame,text='Try speaking like an Avali. Avali are thought to be unable to pronounce the\nfollowing characters due to the lack of a nasal cavity. (Todds Avali Lore Guide)',font=('arial',14), background=Theme[0], foreground=Theme[1])
    SpecialCharsStr = ''
    SpecialReplaceStr = ''
    for i in range(int(len(AP.specialpronchars)/2)):
        SpecialCharsStr += '  '+str(AP.specialpronchars[i*2-1])+' =\n'
    for i in range(len(AP.replacements)):
        if i == 0:
            SpecialReplaceStr += str(AP.replacements[len(AP.replacements)-1])+'\n'
        else:
            SpecialReplaceStr += str(AP.replacements[i-1])+'\n'
    ##Objects
    
    NpronLabel = Label(content_frame,text="N Pronunciation:",font=('arial',14),background=Theme[0],foreground=Theme[1])
    ClampingLabel = Label(content_frame,text="Clamping Characters:",font=('arial',14),background=Theme[0],foreground=Theme[1])
    UPronounceChars = Label(content_frame,text=SpecialCharsStr,font=('arial',16),background=Theme[0],foreground=Theme[1])
    RPronounceChars = Label(content_frame,text=SpecialReplaceStr,font=('arial',16),background=Theme[0],foreground=Theme[1])
    ##Dropdowns
    #HPron
    HpronOptions = ["ha (ha)","Short pause (-)","Short pause (')","Short Pause ( )","Short Pause (,)"] 
    Hdropclicked = StringVar()
    Ndropbutton = OptionMenu( content_frame, Hdropclicked, *HpronOptions)
    Ndropbutton.config(bg=Theme[8],fg=Theme[9]) 
    #Ndropbutton.config(bg=Theme[0])
    Hdropclicked.set(str(HpronOptions[0]))
    #ClampingChars
    ClampingCharsOptions = ['"{-}"(Curvy Brackets)','"[-]"(Brakets)','"|-|"(Line)','"\-"(Backslash)','" - "(Spaces)','"-"(Direct Insert)']
    ClampingCharsSelected = StringVar()
    ClampingCharsButton = OptionMenu(content_frame, ClampingCharsSelected, *ClampingCharsOptions)
    ClampingCharsButton.config(bg=Theme[8],fg=Theme[9]) 
    #Load settings
    CC = str(GO.readIni("Pronunciation","Cchars")) #read the options
    if CC == '0' or CC == '1' or CC == '2' or CC == '3' or CC == '4' or CC == '5' or CC == '6': #if valid entry
        if int(CC) == 0: #Last used 
            #print('Read CC = 0')
            LCC = str(GO.readIni("Pronunciation","LastH")) #read the options
            if LCC == '0' or LCC == '1' or LCC == '2' or LCC == '3' or LCC == '4' or LCC == '5': #if valid entry set the Clamping characters dropdown menu to set option otherwise use the program default
                ClampingCharsSelected.set(str(ClampingCharsOptions[int(LCC)]))
        elif int(CC) <= 6 and int(CC) >= 1: #Default set, set it.
            #print('Read CC =',str(CC-1))
            ClampingCharsSelected.set(str(ClampingCharsOptions[int(CC)-1]))
    else: #else defult horizonta;
        #print('Program Default')
        ClampingCharsSelected.set(str(ClampingCharsOptions[1]))
    HP = str(GO.readIni("Pronunciation","Hpronhars")) #read the options
    if HP == '0' or HP == '1' or HP == '2' or HP == '3' or HP == '4' or HP == '5': #if valid entry set the Clamping characters dropdown menu to set option otherwise use the program default
        if int(HP) == 0: #
            #print('Read HP = 0')
            LHP = str(GO.readIni("Pronunciation","LastH")) #read the options
            if LHP == '0' or LHP == '1' or LHP == '2' or LHP == '3' or LHP == '4': # if valid
                Hdropclicked.set(str(HpronOptions[int(LHP)]))
        elif int(HP) >= 1 and int(HP) <= 5: #
            #print('Read HP =',str(HP-1))
            Hdropclicked.set(str(HpronOptions[int(HP)-1]))
    else: #else defult horizonta;
        #print('HP = Program Default')
        Hdropclicked.set(str(HpronOptions[1]))
    #End Load settings

    ##
    English = Label(content_frame,text=StringVar1,font=('arial',10),background=Theme[0],foreground=Theme[1]) #25 pt lines up with scratch, 20 fits nicely and is about the same size. 
    EnglishO = Label(content_frame,text=StringVar2,font=('arial',20),background=Theme[0],foreground=Theme[1]) #25 pt lines up with scratch, 20 fits nicely and is about the same size. 
    #switch = Button(content_frame,text="minimize")#,command=lambda: )
    Option0 = Button(content_frame,text="4Word",command=lambda: changeText(0),bg=Theme[8],fg=Theme[9])
    Option1 = Button(content_frame,text="6Word",command=lambda: changeText(1),bg=Theme[8],fg=Theme[9])
    Option2 = Button(content_frame,text="sent.",command=lambda: changeText(2),bg=Theme[8],fg=Theme[9])
    Option3 = Button(content_frame,text="para.",command=lambda: changeText(3),bg=Theme[8],fg=Theme[9])
    Option4 = Button(content_frame,text="numb.",command=lambda: changeText(4),bg=Theme[8],fg=Theme[9])
    Option22 = Button(content_frame,text="Custom",command=lambda: changeText(22),bg=Theme[8],fg=Theme[9])
    cInput = Text(content_frame, height = 1, width = 80,bg=Theme[6])
    cInput.bind("<Return>",lambda event: changeText(22))#enterHandler())
    ##Griding
    PronunciationTableHead.grid(column=0,row=0,columnspan=6)
    PronunciationDesc.grid(column=0,row = 1,columnspan=6)
    UPronounceChars.grid(column=6,row = 0,rowspan=3,sticky='e')
    RPronounceChars.grid(column=7,row = 0,rowspan=3,columnspan=2)
    NpronLabel.grid(column=0,row = 2)
    Ndropbutton.grid(column=1,row = 2,columnspan=2)
    ClampingLabel.grid(column=3,row=2)
    ClampingCharsButton.grid(column=4,row=2,columnspan=2)
    border_frame.pack()
    content_frame.grid(column=1,row=0)
    English.grid(column=0,row=5,columnspan=8)
    EnglishO.grid(column=0,row=6,columnspan=8)
    #switch.grid(column=8,row=5)
    Option0.grid(column=1,row=4,sticky='nesw')
    Option1.grid(column=2,row=4,sticky='nesw')
    Option2.grid(column=3,row=4,sticky='nesw')
    Option3.grid(column=4,row=4,sticky='nesw')
    Option4.grid(column=5,row=4,sticky='nesw')
    Option22.grid(column=0,row=4,sticky='nesw')
    cInput.grid(column=0,row=3, columnspan=6,sticky='nesw')
    #cover.grid(column=0,row=0)
    Pwin.mainloop()

def createMainMenuWin(): #This function contains all of the tkinter widgets and functions nececary to be defined before them in order to create the main menu window. Relevent support files: settings.ini
    global MenuImgs
    global Mwin
    #Window Register Management
    if CheckWindowRegister('M') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Mwin = Tk() #Make Main window
    WinCode = AddWindowToRegister(Mwin,'M') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Mwin.configure(background=Theme[2])
    Mwin.title("Avilian Translation Software")
    WindowToTop('M')
    #End Window management

    def selection(inp): #takes button inputs and opens windows coresponding to button indexs
        if inp == 0: #Credits
            createCreditsWin()
        elif inp == 1: #Options
            createOptionsWin()
        elif inp == 2: #text translation Window
            createFontTranslationWin()
        elif inp == 3: #numbers window
            createNumbersWin()
        elif inp == 4: #pronunciation window
            createPronunciationWin()
        else:
            pass

    border_frame = Frame(Mwin,background=Theme[2],borderwidth="4px")
    content_frame = Frame(border_frame, background=Theme[0],borderwidth= "12px")
    Title = Label(content_frame,font=('Helvetica 30 italic'),text="Avalian Translation Software",background=Theme[0],foreground=Theme[3])
    Preface = Label(content_frame,font=('Helvetica 18 italic'),text="By: Renauli Snow",background=Theme[0],foreground=Theme[3]) #Aw du Bub du day. Bah.. Blep.
    Option0 = Button(content_frame,font=('Helvetica 18 italic'),text="  Credits  ",command=lambda: selection(0),background=Theme[2],foreground=Theme[1],activeforeground=Theme[5],activebackground=Theme[4])
    Option1 = Button(content_frame,font=('Helvetica 18 italic'),text="  Options  ",command=lambda: selection(1),background=Theme[2],foreground=Theme[1],activeforeground=Theme[5],activebackground=Theme[4])
    Option2 = Button(content_frame,font=('Helvetica 18 normal'),text="Font Translation",command=lambda: selection(2),background=Theme[2],foreground=Theme[1],activeforeground=Theme[5],activebackground=Theme[4])
    Option3 = Button(content_frame,font=('Helvetica 18 normal'),text="Avalian Numbers",command=lambda: selection(3),background=Theme[2],foreground=Theme[1],activeforeground=Theme[5],activebackground=Theme[4])
    Option4 = Button(content_frame,font=('Helvetica 18 normal'),text="Pronunciation",command=lambda: selection(4),background=Theme[2],foreground=Theme[1],activeforeground=Theme[5],activebackground=Theme[4])
    ##db349c
    border_frame.pack()
    content_frame.pack()
    Title.grid(column=2,columnspan=3,row=0,padx=2,pady=2)
    Preface.grid(column=0,columnspan=5,row=1,padx=3,pady=2)
    Option0.grid(column=2,row=2,columnspan=2,padx=2,pady=2)
    Option1.grid(column=3,row=2,columnspan=2,padx=2,pady=2)
    Option2.grid(column=2,row=3,padx=2,pady=2)
    Option3.grid(column=3,row=3,padx=2,pady=2)
    Option4.grid(column=4,row=3,padx=2,pady=2)
    SidebarMenu.start(Mwin)
    Mwin.mainloop()

'''def createImgMenu(): #delete
    #Window Register Management
    if CheckWindowRegister('T') == False: #Clear creating the window with the register, True means its allowed
        return(False) #killbind
    Iwin = Toplevel(Mwin) #Make window
    WinCode = AddWindowToRegister(Iwin,'T') #Ask to register with the Register, Save Date as unique code.
    if WinCode == False: #If denied
        return(False) #explode
    Iwin.protocol("WM_DELETE_WINDOW", lambda: RemoveWindowFromRegister(Iwin,WinCode,'I')) #Use saved code to remove from register
    Iwin.configure(background=Theme[2])
    #End Window management

    contentFrame = Frame(Iwin)
    #photoholder = Label(contentFrame)
    def spawnImg(sel):
        if sel == 0:
            IMG1 = ImageTk.PhotoImage(Image.open('Images/CapitalLowerCaseCharacters.png'))
            IMG2 = ImageTk.PhotoImage(file= 'Images/SpecialCharacters.png')
            IMG1subtitle = Label(contentFrame,font=('Courier 18 normal'),text='CapitalLowerCaseCharacters.png')
            photoholder = Label(contentFrame,image=IMG2)
            photoholder.grid(column=0,row=0,columnspan=3)
            IMG1subtitle.grid(column=0,row=1)
        elif sel == 1: 
            
            IMG2subtitle = Label(contentFrame,font=('Courier 18 normal'),text='SpecialCharacters.png')
        else:
            print('panic')
    IMG1 = ImageTk.PhotoImage(Image.open('Images/CapitalLowerCaseCharacters.png'))
    IMG2 = ImageTk.PhotoImage(file= 'Images/SpecialCharacters.png')
    IMG1subtitle = Label(contentFrame,font=('Courier 18 normal'),text='CapitalLowerCaseCharacters.png')
    photoholder = Label(contentFrame,image=IMG2)
    photoholder.grid(column=0,row=0,columnspan=3)
    IMG1subtitle.grid(column=0,row=1)
    # https://stackoverflow.com/questions/71677889/create-a-scrollbar-to-a-full-window-tkinter-in-python
    # https://www.google.com/search?q=tkynter+label+image+dimensions&rlz=1C1JSBI_enUS1069US1069&oq=tkynter+label+image+dime&gs_lcrp=EgZjaHJvbWUqCQgBECEYChigATIGCAAQRRg5MgkIARAhGAoYoAEyBwgCECEYqwIyBwgDECEYjwIyBwgEECEYjwLSAQk5ODMzajFqMTWoAgiwAgE&sourceid=chrome&ie=UTF-8
    ### Menubar
    menubar = Menu(Iwin)
    # Create an Window  menu
    windowmenu = Menu(menubar, tearoff=0)
    windowmenu.add_command(label="Font Trans.", command=lambda: createFontTranslationWin())
    windowmenu.add_command(label="Number Trans.", command=lambda: print('createNumberWin()'))
    windowmenu.add_command(label="Pronunciation", command=lambda: print('createPronunciationWin()'))
    menubar.add_cascade(label="Window", menu=windowmenu)
    Imgmenu = Menu(menubar, tearoff=0)
    Imgmenu.add_command(label="Upper+Lowercase Chars.", command=lambda: spawnImg(0))
    Imgmenu.add_command(label="Special Chars.", command=lambda: spawnImg(1))
    Imgmenu.add_command(label="Cause an error", command=lambda: spawnImg(3))
    menubar.add_cascade(label="Images", menu=Imgmenu)
    Iwin.config(menu=menubar)
    #photoholder.grid(column=0,row=0,columnspan=3)
    contentFrame.pack()

    Iwin.mainloop()'''




'''def teststart():
    #createCreditsWin()
    #createOptionsWin()
    #createFontTranslationWin()
    createNumbersWin()
    #createPronunciationWin()
    #createMainMenuWin()
    #createImgMenu()''' #No longer works due to relyiance on Mwin
createMainMenuWin() #Anything after this will not execute