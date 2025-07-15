specialpronchars = ['f','F','j','J','n','N','v','V']
replacements = ['y-ah','bu','short pause or "ha" sound','hthk'] #
#abcde ghi klm opqrstu wxyz  Present
#    f    j   n       v      Missing

#functions


def pronounciationDisp(ntext,npron,clampingchars):
    Npron = npron.split(' ') 
    Npron = Npron[len(Npron)-1].replace('(','').replace(')','')
        #
    ClampingChars = clampingchars.split('"(')
    ClampingChars = ClampingChars[0].replace('"',"").split('-')
    ClampingCharL,ClampingCharR = ClampingChars
    #print(ClampingCharL)
    #print(ClampingCharR)
    #print("Npron:",Npron)
    #rint("Executing...")
    digest = ntext.split(' ')
    for i in range(len(digest)): #for each word 
        word = list(digest[i])
        wWord = word #split current word into letters
        for k in range(len(wWord)): #for each leter
            for t in range(int((len(specialpronchars)))):#check if match a special character 
                if t+1 % 3 != 0:
                    #print(specialpronchars[t])
                    if wWord[k] == specialpronchars[t]:
                        #print('Detected Illegal:',word[k],'   Flagged as:',specialpronchars[t])
                        if t+1 % 2 == 0: #if odd index (even adjuseted)  
                            #print("SpecPro:",specialpronchars[t],"Replace:",replacements[(t/2)-2])
                            
                            word[k] = ClampingCharL+replacements[(t/2)-1]+ClampingCharR
                        else:
                            #print("SpecPro:",specialpronchars[t],"Replace:",replacements[int((t/2))])
                            if replacements[int((t/2))] == 'short pause or "ha" sound':
                                word[k] = ClampingCharL+Npron+ClampingCharR
                            else:
                                word[k] = ClampingCharL+replacements[int((t/2))]+ClampingCharR
        word = "".join(word)
        digest[i] = word 
        betwener = ' '
        ajoinedDigest = betwener.join(digest)
    print("Completed.")
    print(digest)
    print(ajoinedDigest)
    return(ajoinedDigest)

#pronounciationDisp("f j n v ",'Short Pause (-)','"{-}"(Curvy Brackets)')
#pronounciationDisp("The quick brown fox jumped over the lazy frog.")
