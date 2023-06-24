import os
if(os.path.exists("localbody_queries.py")):
    os.remove("localbody_queries.py")
else:
    print("File doesn't exist!")


dobj ="=District.objects.get(id="
lbcat ="=LocalBodyCategory.objects.get(id="

with open("localBodies.csv","r") as dfp:
    regions = dfp.readlines()
    for region in regions:
        reglist = region.split(',')
        #print(reglist)

        if(reglist[4].strip()==''):
            ward = str(12)
        else:
            ward = str(reglist[4].strip())
        line="LocalBody(id="+str(reglist[0].strip())+", district"+dobj+str(reglist[1].strip())+"), name=\""+str(reglist[2].strip())+"\", category"+lbcat+str(reglist[3].strip())+"), num_wards="+ward+", new_old="+str(reglist[5].strip())+").save()\n"

        print(line.strip())
        with open("localbody_queries.py","a") as dque:
            dque.write(line)
