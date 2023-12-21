# spectral discretization
import sys
INF = 1000000000 
spectralMaxima = 20
pathspreadlimit = 9
a = 40 # need to configure it also 

if len(sys.argv) < 3:
    # print("Usage: python script.py input_file1.txt input_file2.txt input_file3.txt")
    sys.exit(1)

gateDelaysAndAreas = {}
ndaa = {} #tells the delay and area of the current node
# node delays and areas
outputMinAreas = {}
nodeadj = {} #will store previous nodes
prevnodeadj = {}
assignedIndex = {}
# Will store the final areas assigned after optimizing all the paths : 
primaryinputs = []
primaryoutputs = []
delayconstraint = 0
active = {}
maxdelay = INF
case = sys.argv[1]
if case == 'B' :
    loc = sys.argv[5]
    dc = sys.argv[4]
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
    gd = sys.argv[3]
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
                maxdelay = min(maxdelay,float(data[2]))
            else : 
                gateDelaysAndAreas[data[1]] = [[float(data[2]),float(data[3])]]
                maxdelay = min(maxdelay,float(data[2]))
    # print (gateDelaysAndAreas)
    ckt = sys.argv[2]
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

                    if data[n - 1] not in prevnodeadj:
                        prevnodeadj[data[n - 1]] = [[], -1]
                    prevnodeadj[data[n - 1]][0].append(data[i])

    ####################### Remove before debugging #########
    n = len(ndaa)
    spectralMaxima = maxdelay * n
    spectralMaxima = min(float(delayconstraint)+10,float(spectralMaxima))
    a = 1000000/(n*n*10)
    a = max(round(int(a),2),100)
    if(n < 11) : 
        # print("Ran 3^n algorithm...")
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
            # print(string)
            # print(active)
        maxi = 0
        def process() : 
            global maxi
            for output in primaryoutputs : 
                maxi = max(maxi,run(output))
            for node in prevnodeadj : 
                prevnodeadj[node][1] = -1
            return maxi
        def run(node):
            if node in primaryinputs:
                return 0.0
            elif prevnodeadj[node][1] != -1:
                return prevnodeadj[node][1]
            else:
                for child in prevnodeadj[node][0]:
                    prevnodeadj[node][1] = max(prevnodeadj[node][1], run(child))
                prevnodeadj[node][1] += ndaa[node][active[node]][0]
                return prevnodeadj[node][1]  
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
            # print("Process is (for checking gate delays): ",process())
            if(process() <= float(delayconstraint)) : 
                area = calcarea()
                # print("Calculated area is : ",area)
                minarea = min(minarea,area)

        # print(minarea)
        with open(loc, 'w') as Myfile:
            if minarea%1 == 0:
                Myfile.write(f"{int(minarea)}")
            else:
                Myfile.write(f"{minarea}")
    else : 
        # Needs optimization
        # Provides a lower limit of any value supplied.
        ###################################################
        # binedges = [0]
        # for i in range (1,a) : 
        #     binedges.append(i * spectralMaxima/(a))
        # binedges.append(spectralMaxima)
        # print(binedges)
        # def descretize(value):
        #     global binedges
        #     if float(value) < 0 : 
        #         return -34404
        #     for i,edge in enumerate(binedges):
        #         if float(value) < edge : 
        #             return i-1
        #     return len(binedges) - 1
        # def continize(value) : 
        #     global binedges
        #     return binedges[value]
        ##################################################
        binedges = {}
        edgebin = {}
        for i in range(a + 2):
            upper_limit = i * spectralMaxima / a
            binedges[i] = upper_limit  # Use 0-based indexing
            edgebin[upper_limit] = i
        def descretize(value):
            if float(value) < 0:
                return 0
            for i, edge in binedges.items():
                if float(value) < edge:
                    return i-1
            return len(binedges) - 2  # Adjust for the 0-based indexing
        def continize(index):
            if index not in binedges:
                return 0  # Handle invalid index
            return binedges[index]
        #######################################################
        # run the path generator for all the primary inputs.
        pathspreadcount = 0
        currentpath = []
        localminima = INF
        def pathgenerator(current) : 
            global localminima,pathspreadcount,pathspreadlimit
            if pathspreadcount > pathspreadlimit : 
                return localminima
            if (len(currentpath) == 0):
                currentpath.append(current)
            if current in primaryoutputs : 
                # print (currentpath)
                localminima = min(localminima,process(currentpath))
                pathspreadcount = pathspreadcount + 1
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
            # print("n is : ",n)
            # Initialize data structures for DP and backtracking
            dp = [[INF] * (a + 1) for _ in range(n + 1)]
            selected_values = [[-1] * (a + 2) for _ in range(n + 2)]

            dp[0][0] = 0
            # print(path)
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
            #         print(dp[i][j]," ",end="")
            #     print("") 
            # print(selected_values)
            # print("delay constraint is : ",(delayconstraint))
            # print("Final value returned : ",dp[n][descretize(delayconstraint)])
            # Backtrack to find which values were assigned
            assigned_values = []
            j = descretize(delayconstraint)
            for i in range(n, 0, -1):
                k = selected_values[i][j]
                assigned_values.append(k)
                j = descretize(continize(j) - ndaa[path[i - 1]][k][0])
            assigned_values.reverse()
            # print("assigned values are : ",assigned_values)
            assignedIndex[path[0]] = 0
            for i in range(1,n) : 
                if path[i] not in assignedIndex : 
                    assignedIndex[path[i]] = assigned_values[i]
                else : 
                    if (ndaa[path[i]][assignedIndex[path[i]]][1]<ndaa[path[i]][assigned_values[i]][1]) : 
                        assignedIndex[path[i]] = assigned_values[i]
            return dp[n][a]

        # after processing, answer will be dp[n,descretize(limit)]
        def calcfinaldelay(node):
            if node in primaryinputs:
                return 0.0
            elif prevnodeadj[node][1] != -1:
                return prevnodeadj[node][1]
            else:
                for child in prevnodeadj[node][0]:
                    prevnodeadj[node][1] = max(prevnodeadj[node][1], calcfinaldelay(child))
                prevnodeadj[node][1] += ndaa[node][assignedIndex[node]][0]
                return prevnodeadj[node][1]
        finaldelay = 0
        def finaldelaycalculator() : 
            global finaldelay
            # for node in primaryoutputs : 
                # finaldelay = max(finaldelay,calcfinaldelay(node))   testing
            return finaldelay

        minarea = 0
        for first in primaryinputs:
            # calls all the processes and ensures max optimization.
            pathgenerator(first)
        # assign the values not assigned even after processes : 
        for node in ndaa : 
            if (node not in assignedIndex) : 
                value = ndaa[node][0][1]
                if (ndaa[node][1][0] < ndaa[node][0][0]) : 
                    value = ndaa[node][1][1]
                elif ((ndaa[node][2][0] < ndaa[node][1][0]) and (ndaa[node][2][0] < ndaa[node][1][0])) :
                    value = ndaa[node][2][1] 

        # check finally if the things agree : 
        delayfinal = finaldelaycalculator()
        # print(delayfinal)
        if (delayfinal > float(delayconstraint)) : 
            minarea = -1
        else : 
            for index in assignedIndex: 
                minarea += ndaa[index][assignedIndex[index]][1]

        # print (assignedIndex)
        # print(minarea)
        with open(loc, 'w') as Myfile:
            if minarea%1 == 0:
                Myfile.write(f"{int(minarea)}")
            else:
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
elif (case == 'A') :
    dc = sys.argv[4] 

    gd = sys.argv[3]
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
                    if (float(data[2]) < gateDelaysAndAreas[data[1]][0]) :
                        gateDelaysAndAreas[data[1]] = [float(data[2]),float(data[3])] 
                else : 
                    gateDelaysAndAreas[data[1]] = [float(data[2]),float(data[3])]
    ckt = sys.argv[2]
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
                    ndaa[data[i]] = [0,0]
                elif data[0] == "PRIMARY_OUTPUTS":
                    primaryoutputs.append(data[i])
                    outputMinAreas[data[i]] = -1
                elif data[0] == "INTERNAL_SIGNALS":
                    pass
                elif data[0] == "DFF":
                    primaryinputs.append(data[2])
                    ndaa[data[2]] = [0,0]
                    primaryoutputs.append(data[1])
                    break
                else:
                    if i == n-1:
                        break
                    if data[n - 1] not in nodeadj:
                        nodeadj[data[n - 1]] = [[], -1]
                    nodeadj[data[n - 1]][0].append(data[i])
                    ndaa[data[n - 1]] = gateDelaysAndAreas[data[0]]
    value = 0
    # print(gateDelaysAndAreas)
    # print(ndaa)
    # print(nodeadj)
    def run(node):
        if node in primaryinputs:
            return 0.0
        elif nodeadj[node][1] != -1:
            return nodeadj[node][1]
        else:
            for child in nodeadj[node][0]:
                nodeadj[node][1] = max(nodeadj[node][1], run(child))
            nodeadj[node][1] += ndaa[node][0]
            return nodeadj[node][1]
    
    delay = 0
    for last in primaryoutputs:
        for node in nodeadj : 
            nodeadj[node][1] = -1
        value = run(last)
        # print(last," ",value)
        delay = max(delay,value)
    with open(dc, 'w') as Myfile:
        if delay%1 == 0:
            Myfile.write(f"{int(delay)}")
        else:
            Myfile.write(f"{delay}")
