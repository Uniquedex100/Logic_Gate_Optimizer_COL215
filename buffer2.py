import sys
INF = 1000000000

if len(sys.argv) < 3:
    print("Usage: python script.py input_file1.txt input_file2.txt input_file3.txt")
    sys.exit(1)

gateDelaysAndAreas = {}
nodeDelaysAndAreas = {} #tells the delay and area of the current node
outputMinAreas = {}
nodeadj = {} #will store previous nodes
#No benefit of storing minareas, as they will vary according to currentConstraint
primaryinputs = []
primaryoutputs = []
delayconstraint = 0
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
        for i in range(len(data)):
            if(data[1] in gateDelaysAndAreas) :
                gateDelaysAndAreas[data[1]].append([data[2],data[3]])

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
            elif data[0] == "PRIMARY_OUTPUTS":
                primaryoutputs.append(data[i])
                outputMinAreas[data[i]] = -1
            elif data[0] == "INTERNAL_SIGNALS":
                pass
            elif data[0] == "DFF":
                primaryinputs.append(data[2])
                primaryoutputs.append(data[1])
            else:
                if i == n-1:
                    break
                if data[n - 1] not in nodeadj:
                    nodeadj[data[n - 1]] = []
                nodeadj[data[n - 1]].append(data[i])
                nodeDelaysAndAreas[data[n - 1]] = gateDelaysAndAreas[data[0]]

value = 0
def run(node,currentConstraint): # returns the min area corresponding to limit of delay as currentConstraint
    if node in primaryinputs:
        return 0.0
    else:
        for child in nodeadj[node]:
            nodeadj[node][1] = max(nodeadj[node][1], run(child))
        nodeadj[node][1] += nodeDelaysAndAreas[node]
        return nodeadj[node][1]
    
minarea = INF
for last in primaryoutputs:
    for i in range (0,len(nodeDelaysAndAreas)) : 
        outputMinAreas[last] = run(last,delayconstraint - nodeDelaysAndAreas[last][i][0])
    minarea = min(minarea,outputMinAreas[last])
with open("longest_delay.txt", 'w') as Myfile:
    Myfile.write(f"{minarea}")

# Algorithm: 
# 