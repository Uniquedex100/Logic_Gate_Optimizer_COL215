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
assignedIndex = {}
# Will store the final areas assigned after optimizing all the paths : 
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
                if data[i] not in nodeadj:
                    nodeadj[data[i]] = []
                nodeadj[data[i]].append(data[n - 1])
                ndaa[data[n - 1]] = gateDelaysAndAreas[data[0]]

# Needs optimization
# Provides a lower limit of any value supplied.
binedges = [0]
for i in range (1,a) : 
    binedges.append(i * spectralMaxima/(a))
binedges.append(spectralMaxima)
print(binedges)
def descretize(value):
    global binedges
    if float(value) < 0 : 
        return -34404
    for i,edge in enumerate(binedges):
        if float(value) < edge : 
            return i-1
    return len(binedges) - 1

def continize(value) : 
    global binedges
    return binedges[value]

# run the path generator for all the primary inputs.
currentpath = []
localminima = INF
def pathgenerator(current) : 
    global localminima
    if (len(currentpath) == 0):
        currentpath.append(current)
    if current in primaryoutputs : 
        # print (currentpath)
        localminima = min(localminima,process(currentpath))
    else :
        for next in nodeadj[current]:
            currentpath.append(next)
            pathgenerator(next)
    currentpath.pop()
    return localminima

# ndaa structure : 
# maps gatetype to list of (delay1,area1),(delay2,area2),(delay3,area3).
# ndaa[key][0,1 or 2][delay or area]

# processing the current path.
dp = []
backtrack = []
def process(path):
    global backtrack, a
    n = len(path)
    print("n is : ",n)
    # Initialize data structures for DP and backtracking
    dp = [[INF] * (a + 1) for _ in range(n + 1)]
    selected_values = [[-1] * (a + 1) for _ in range(n + 1)]

    dp[0][0] = 0
    print(path)
    for i in range(0, n + 1):
        for j in range(a + 1):
            continized_j = continize(j)
            if i == 0 : 
                dp[i][j] = 0 
            else : 
                for k in range(3):
                    if continized_j - ndaa[path[i - 1]][k][0] >= 0:
                        temp = ndaa[path[i - 1]][k][1] + dp[i - 1][descretize(continized_j - ndaa[path[i - 1]][k][0])]
                        if temp < dp[i][j]:
                            dp[i][j] = temp
                            selected_values[i][j] = k
            print(dp[i][j]," ",end="")
        print("") 
    print(selected_values)
    print("delay constraint is : ",descretize(delayconstraint))
    print("Final value returned : ",dp[n][descretize(delayconstraint)])

    # Backtrack to find which values were assigned
    assigned_values = []
    j = descretize(delayconstraint)
    for i in range(n, 0, -1):
        k = selected_values[i][j]
        assigned_values.append(k)
        j = descretize(continize(j) - ndaa[path[i - 1]][k][0])
    
    assigned_values.reverse()
    print("assigned values are : ",assigned_values)

    assignedIndex[path[0]] = 0
    for i in range(1,n) : 
        if path[i] not in assignedIndex : 
            assignedIndex[path[i]] = assigned_values[i]
        else : 
            if (ndaa[path[i]][assignedIndex[path[i]]][1]<ndaa[path[i]][assigned_values[i]][1]) : 
                assignedIndex[path[i]] = assigned_values[i]
    return dp[n][a]

# after processing, answer will be dp[n,descretize(limit)]

# value = 0
# def run(node):
#         if node in primaryinputs:
#             return 0.0
#         elif nodeadj[node][1] != -1:
#             return nodeadj[node][1]
#         else:
#             for child in nodeadj[node][0]:
#                 nodeadj[node][1] = max(nodeadj[node][1], run(child))
#             nodeadj[node][1] += ndaa[node]
#             return nodeadj[node][1]
    
minarea = 0
for first in primaryinputs:
    # print("Calling pathgenerator for ",first)
    pathgenerator(first)
for index in assignedIndex: 
    minarea += ndaa[index][assignedIndex[index]][1]
print (assignedIndex)
print(minarea)
with open("minimum_area.txt", 'w') as Myfile:
    Myfile.write(f"{minarea}")

# Algorithm: 
# Isolate every possible path : O(n^2)
#   maintain a vector of the vertices?
# Assume max length of each path to be O(n)
# o -> o -> o -> o -> o -> o
# apply dp(i,j) formula
# find the value of dp(n,limit)
# dp(i,j) is going to be a matrix consisting of n rows and a columns.
# columns are nothing but discretized areas.
# a = 1e6 / n^3
# So we need to divide area spectrum into a parts
# area spectrum maxima needs to be set. (can be improved a lot) 
# dp[i][j] denotes the minarea counting nodes till i and having maxdelay limit as j.