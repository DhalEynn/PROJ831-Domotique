def listToString(s):  
    # initialize an empty string 
    str1 = ""  
    # traverse in the string   
    for ele in s:  
        str1 += ele + " "    
    # return string   
    return str1  

def LineReadingFromFile(inputFile):
    """
    Filtering and formatting the log file
    in: inputFile textfile that contain the log to filter
    out: array of dictionnary, one dictionnary for each line
    """
    FormattedData=[] 

    with open(inputFile, 'r') as openfileobject:
        # Browse line per line
        for line in openfileobject:
            UpperLine = line.upper()
            # Keep lines that contains WGRAPH and an associated date
            filteredLine=filtering(UpperLine)
            if filteredLine != '':

                # Formate Lines
                FormattedData.append(formattingData(filteredLine))
    return FormattedData

def filtering(UpperLine):
    """
    Filter the line and keep it only if the line  contain WGRAPH and an associated date
    in: the Line in upper character (str)
    out: return '' when the line is blocked and the filtered line if it go through (str)
    """
    if "WGRAPH" in UpperLine:
        splittedLine = UpperLine.split(' ')
        filteredLine = listToString(splittedLine[3:])
        if "DATES" in filteredLine:
            return filteredLine
    return ''
            
def formattingData(filteredLine):
    """
    Formate the filtered line
    in: filtered line (str)
    out: dictionnary of the line exemple: { 'category': 'switch', 'Id': 7, 'fonction': 'HEAT', 'action': 'TRY TO RUN EDGE', 'Begin State': [1, True],     'command': 'OFF',     'Ending State': [1, False], 'Begin Date': 485, 'Ending Date': 486 }
    """
    splittedLine1 = filteredLine.split(':')
    state=splittedLine1[3].split('->')
    splitIdFunction=splittedLine1[1].split(' ')
    # Create the dictionnary
    formattedLine = {'Category':splittedLine1[0].split('.')[-1],\
        'Id':int(splitIdFunction[0]),\
        'Function':splitIdFunction[1][1:-2],\
        'Action':splittedLine1[2][1:]}

    # Handle the case when there is no ending states
    if len(state)==3:
        splitDate =splittedLine1[-1].split(' TO ')
        formattedLine['Begin State']=state[0][1:]
        formattedLine['Command']=state[1]
        formattedLine['Ending State']=state[2].split(' B')[0]
        formattedLine['Begin Date']=int(splitDate[0][1:])
        formattedLine['Ending Date']=int(splitDate[1][:-2])
        
    else:
        splitDate =splittedLine1[-1].split(' TO ')
        formattedLine['Begin State']=splittedLine1[3].split(' B')[0][1:]
        formattedLine['Begin Date']=int(splittedLine1[-1].split(';')[0][2:])
        formattedLine['Ending Date']=int(splittedLine1[-1].split(';')[1][:-3])
    return formattedLine
