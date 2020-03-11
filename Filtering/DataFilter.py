
def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele + " "    
    
    # return string   
    return str1  


def LineReadingFromFile(inputFile):
    """Filter the log data, keep only the lines that contain WGRAPH
        in: inputFile textfile that contain the log to filter
        out: outputFile textfile where your filtered logs will be writed
    """
    JsonFormattedData=[] 
    # file browse

    with open(inputFile, 'r') as openfileobject:
        for line in openfileobject:
            UpperLine = line.upper()
            filteredLine=filtering(UpperLine)
            if filteredLine != '':
                JsonFormattedData.append(formattingData(filteredLine))
    return JsonFormattedData
    


def filtering(UpperLine):
    if "WGRAPH" in UpperLine:
        splittedLine = UpperLine.split(' ')
        filteredLine = listToString(splittedLine[3:])
        if "DATES" in filteredLine:
            return filteredLine
    return ''
            

def formattingData(filteredLine):
    
    splittedLine1 = filteredLine.split(':')
    state=splittedLine1[3].split('->')

    formattedLine = {'Category':splittedLine1[0].split('.')[-1],\
        'Id':int(splittedLine1[1].split(' ')[0]),\
        'Function':splittedLine1[1].split(' ')[1][1:-2],\
        'Action':splittedLine1[2][1:]}
    if len(state)==3:

        formattedLine['Begin State']=state[0][1:]
        formattedLine['Command']=state[1]
        formattedLine['Ending State']=state[2].split(' B')[0]
        formattedLine['Begin Date']=int(splittedLine1[-1].split(' TO ')[0][1:])
        formattedLine['Ending Date']=int(splittedLine1[-1].split(' TO ')[1][:-2])
        
    else:
        formattedLine['BeginState']=splittedLine1[3].split(' B')[1:]
        formattedLine['BeginDate']=int(splittedLine1[-1].split(';')[0][2:])
        formattedLine['Ending Date']=int(splittedLine1[-1].split(';')[1][:-2])
    return formattedLine
print(LineReadingFromFile('Files/test.log'))


