import os
if(os.path.exists("localbodytype_queries.py")):
    os.remove("localbodytype_queries.py")
else:
    print("File doesn't exist!")


with open("LocalBodyTypes.csv","r") as dfp:
    regions = dfp.readlines()
    for region in regions:
        reglist = region.split(',')
        #print(reglist)

        line="LocalBodyCategory(id="+str(reglist[0].strip())+", name=\""+str(reglist[1].strip())+"\", new_old="+str(reglist[2].strip())+").save()\n"

        print(line.strip())
        with open("localbodytype_queries.py","a") as dque:
            dque.write(line)
