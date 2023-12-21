# spectral discretization
import sys
INF = 1000000000 
spectralMaxima = 20
a = 20 # need to configure it also 

if len(sys.argv) < 3:
    print("Usage: python script.py input_file1.txt input_file2.txt input_file3.txt")
    sys.exit(1)

gateDelaysAndAreas = {}
ndaa = {} #tells the delay and area of the current node
# node delays and areas
outputMinAreas = {}
nodeadj = {} #will store previous nodes
#No benefit of storing minareas, as they will vary according to currentConstraint
assignedAreas = {}
# Will store the final areas assigned after optimizing all the paths : 
primaryinputs = []
primaryoutputs = []
delayconstraint = 0
active = {}
dc = sys.argv[3]
with open(dc,'r') as in3:
    for line in in3 : 
        text = line.strip()
        if not text:
            continue
        if text.startswith('//'):
            continue
        if text[0] == ' ':
            continue
        data = text.split()
        delayconstraint = data[0]

gd = sys.argv[2]
with open(gd,'r') as in1:
    for line in in1:
        text = line.strip()
        if not text:
            continue
        if text.startswith('//'):
            continue
        if text[0] == ' ':
            continue
        data = text.split()
        init = data[0]
        if(data[1] in gateDelaysAndAreas) :
            gateDelaysAndAreas[data[1]].append([float(data[2]),float(data[3])])
        else : 
            gateDelaysAndAreas[data[1]] = [[float(data[2]),float(data[3])]]

# print (gateDelaysAndAreas)

ckt = sys.argv[1]
with open(ckt,'r') as in2:
    for line in in2:
        text = line.strip()
        if not text:
            continue
        if text.startswith('//'):
            continue
        if text[0] == ' ':
            continue
        data = text.split()
        n = len(data)
        for i in range(1, len(data)):
            if data[0] == "PRIMARY_INPUTS":
                primaryinputs.append(data[i])
                # print ("appended ",data[i])
                ndaa[data[i]] = [[0,0],[0,0],[0,0]]
            elif data[0] == "PRIMARY_OUTPUTS":
                primaryoutputs.append(data[i])
                outputMinAreas[data[i]] = -1
            elif data[0] == "INTERNAL_SIGNALS":
                pass
            elif data[0] == "DFF":
                primaryinputs.append(data[2])
                # print("appended ",data[2])
                ndaa[data[2]] = [[0,0],[0,0],[0,0]]
                primaryoutputs.append(data[1])
                break
            else:
                if i == n-1:
                    break
                if data[n - 1] not in nodeadj:
                    nodeadj[data[n - 1]] = [[], -1]
                nodeadj[data[n - 1]][0].append(data[i])
                ndaa[data[n - 1]] = gateDelaysAndAreas[data[0]]

n = len(ndaa)

for node in ndaa : 
    active[node] = 0

def int_to_base3(n):
    if n == 0:
        return '0'
    base3_string = ""
    while n > 0:
        remainder = n % 3
        base3_string = str(remainder) + base3_string
        n = n // 3
    # print(base3_string)
    return base3_string

def alter(i) : 
    string = int_to_base3(i)
    j = 0
    for node in active : 
        if(len(string)-1 < j) : 
            active[node] = 0
        elif(string[len(string)-j-1] == '0') : 
            active[node] = 0
        elif(string[len(string)-j-1] == '1') : 
            active[node] = 1
        else : 
            active[node] = 2
        j = j+1
    print(string)
    print(active)

maxi = 0
def process() : 
    global maxi
    for output in primaryoutputs : 
        maxi = max(maxi,run(output))
    for node in nodeadj : 
        nodeadj[node][1] = -1
    return maxi
def run(node):
    if node in primaryinputs:
        return 0.0
    elif nodeadj[node][1] != -1:
        return nodeadj[node][1]
    else:
        for child in nodeadj[node][0]:
            nodeadj[node][1] = max(nodeadj[node][1], run(child))
        nodeadj[node][1] += ndaa[node][active[node]][0]
        return nodeadj[node][1]
    
areasum = 0
def calcarea() :
    global areasum
    for node in ndaa : 
        areasum += ndaa[node][active[node]][1]
    return areasum

minarea = INF
for i in range(0,pow(3,n)) : 
    maxi = 0
    areasum = 0
    alter(i)
    print("Process is (for checking gate delays): ",process())
    if(process() <= int(delayconstraint)) : 
        area = calcarea()
        print("Calculated area is : ",area)
        minarea = min(minarea,area)

print(minarea)
with open("minimum_area.txt", 'w') as Myfile:
    Myfile.write(f"{minarea}")