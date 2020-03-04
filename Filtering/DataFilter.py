def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele + " "    
    
    # return string   
    return str1  


def filtering(inputFile, outputFile):
    """Filter the log data, keep only the lines that contain WGRAPH
        in: inputFile textfile that contain the log to filter
        out: outputFile textfile where your filtered logs will be writed
    """
    log_out = open(outputFile, "w") 
    line_count=0
    # file browse
    with open(inputFile, "r") as openfileobject:
        for line in openfileobject:
            UpperLine = line.upper()
            
            if "WGRAPH" in UpperLine:
                splittedLine = UpperLine.split(" ")
                filteredLine = listToString(splittedLine[3:])
                log_out.write(filteredLine)
                line_count+=1
    log_out.write(str(line_count) + " line created") 
    log_out.close()


def getDate(inputFile, outputFile):
    log_out = open(outputFile, "w") 
    line_count=0
    with open(inputFile, "r") as openfileobject:
        for line in openfileobject:
            UpperLine = line.upper()
            
            if "DATES" in UpperLine:
                log_out.write(UpperLine)
                line_count+=1
    log_out.write(str(line_count) + " line created") 
    log_out.close()

filtering("Files/test.log", "Files/testClean.log")
getDate("Files/testClean.log", "Files/testDate.log")

