import os
if(os.path.exists("region_queries.py")):
    os.remove("region_queries.py")
else:
    print("File doesn't exist!")


with open("Region.csv","r") as rfp:
    regions = rfp.readlines()
    for region in regions:
        reglist = region.split(',')
        #print(reglist)
        line = "Region(id=" + str(reglist[0].strip()) + ", name=\""+str(reglist[1].strip())+"\", new_old="+str(reglist[2].strip())+").save()\n"
        print(line.strip())
        
        with open("region_queries.py","a") as rque:
            rque.write(line)
