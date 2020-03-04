log_out = open("Files/FilteredData.txt", "w") 
line_count=0
with open("Files/WOF.log", "r") as openfileobject:
    for line in openfileobject:
        line=line.upper()
        
        if "WGRAPH" in line:
            log_out.write(line)
            line_count+=1
log_out.write(str(line_count) + " line created") 
log_out.close()