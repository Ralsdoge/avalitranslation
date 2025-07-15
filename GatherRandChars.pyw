import random
from GatherOptions import absolute_path,errorMsg
rawData = ""
try:
    #nonlocal rawData
    with open(absolute_path("random.md")) as randomData:
        rawData = randomData.read().splitlines()
except:
    errorMsg('random.md missing','The file "random.md" is missing, please replace random.md or reinstall program.')
    BackupData = "#0-4word\nrandom.md missing\n#1-6word\nrandom.md missing\n#2-Sentences\nrandom.md missing\n#3-Paragraps\nrandom.md missing\n"
    rawData = BackupData.splitlines()
def myFunc(e):
    return e['year']
all = []
workingEvents = []
fourWord = []
sixWord = []
sentences = []
paragraphs = []
numbers = []
SampleList0=[]
SampleList1=[]
SampleList2=[]
SampleList3=[]
SampleList4 =[]
NewC = ''
class event():
    def __init__(self,iname,itype):
        self.type = itype
        self.name = iname
        if self.type == '0':
            fourWord.append(self)
        if self.type == '1':
            sixWord.append(self)
        if self.type == '2':
            sentences.append(self)
        if self.type == '3':
            paragraphs.append(self)
        if self.type == '4':
            numbers.append(self)

    def read(self,select=5):
        if select == 1:
            return(self.type)
        elif select == 2:
            return(self.name)
        else:
            return(self.type,self.name)
        
def ChallengeRandSample(type): #line 49
    global SampleList0
    global SampleList1
    global SampleList2
    global SampleList3
    global SampleList4
    global NewC
    global all
    if type == 0:
        if len(SampleList0) == 0:
            SampleList0 = random.sample(fourWord,len(fourWord))
        NewC = str(event.read(SampleList0[0],2))
        SampleList0.pop(0)
        return(NewC)
    if type == 1:
        if len(SampleList1) == 0:
            SampleList1 = random.sample(sixWord,len(sixWord))
        NewC = str(event.read(SampleList1[0],2))
        SampleList1.pop(0)
        return(NewC)
    if type == 2:
        if len(SampleList2) == 0:
            SampleList2 = random.sample(sentences,len(sentences))
        NewC = str(event.read(SampleList2[0],2))
        SampleList2.pop(0)
        return(NewC)
    if type == 3:
        if len(SampleList3) == 0:
            SampleList3 = random.sample(paragraphs,len(paragraphs))
        NewC = str(event.read(SampleList3[0],2))
        SampleList3.pop(0)
        return(NewC)
    if type == 4:
        if len(SampleList4) == 0:
            SampleList4 = random.sample(numbers,len(numbers))
        NewC = str(event.read(SampleList4[0],2))
        SampleList4.pop(0)
        return(NewC)
    
    return('blank')


curType = 'Unknown'
for line in rawData:
   
    #Pair = line.splitlines()
    #Pair = line.split(':')
    #print(Pair)
    #if ',' in line:
        #Date = Pair[1].split(',')
        #event(Pair[0],Date[0],curType)
    if '#' in line:
        curType = line.strip('#')
        pair=curType.split('-')
        curType = pair[0]
    elif line == '':
        pass
    else:
        event(line,curType)
#events.sort(key=lambda x: x.order, reverse=False)
#print(len(paragraphs),' items registered')
#for item in all:
#    print(item.read(1))

