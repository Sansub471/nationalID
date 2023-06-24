import os
if(os.path.exists("district_queries.py")):
    os.remove("district_queries.py")
else:
    print("File doesn't exist!")


with open("Districts.csv","r") as dfp:
    regions = dfp.readlines()
    for region in regions:
        reglist = region.split(',')
        #print(reglist)

        regGet = "=Region.objects.get(id="

        zn = reglist[2].strip()
        pn = reglist[3].strip()

        if( zn == "NULL"):
            zone=""
        else:
            zone=", zone" + regGet+str(reglist[2].strip()) +")"
        
        if( pn == "NULL"):
            prov=""
        else:
            prov=", province"+regGet+str(reglist[3].strip()) + ")"
        


        line = "District(id="+str(reglist[0].strip())+", name=\""+str(reglist[1].strip())+"\""+zone+prov+").save()\n"

        print(line.strip())
        with open("district_queries.py","a") as dque:
                dque.write(line)
