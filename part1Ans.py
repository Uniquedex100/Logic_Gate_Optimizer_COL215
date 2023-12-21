import sys
INF = 1000000000

if len(sys.argv) < 2:
    print("Usage: python script.py A input_file1.txt input_file2.txt")
    print("or")
    print("Usage: python script.py B input_file1.txt input_file2.txt input_file3.txt")
    sys.exit(1)

keyword = sys.argv[1]
if keyword == "A":
    gatedelays = {}
    nodedelay = {}
    outputdelay = {}
    nodeadj = {} #will store previous nodes as well as current delay
    primaryinputs = []
    primaryoutputs = []
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
                if(data[1] in gatedelays) :
                    gatedelays[data[1]] = min(gatedelays[data[1]],float(data[2]))
                else : 
                    gatedelays[data[1]] = float(data[2])

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
                elif data[0] == "PRIMARY_OUTPUTS":
                    primaryoutputs.append(data[i])
                    outputdelay[data[i]] = -1
                elif data[0] == "INTERNAL_SIGNALS":
                    pass
                elif data[0] == "DFF":
                    primaryinputs.append(data[2])
                    primaryoutputs.append(data[1])
                else:
                    if i == n-1:
                        break
                    if data[n - 1] not in nodeadj:
                        nodeadj[data[n - 1]] = [[], -1]
                    nodeadj[data[n - 1]][0].append(data[i])
                    nodedelay[data[n - 1]] = gatedelays[data[0]]

    value = 0
    def run(node):
        if node in primaryinputs:
            return 0.0
        elif nodeadj[node][1] != -1:
            return nodeadj[node][1]
        else:
            for child in nodeadj[node][0]:
                nodeadj[node][1] = max(nodeadj[node][1], run(child))
            nodeadj[node][1] += nodedelay[node]
            return nodeadj[node][1]
    final_answer = 0
    for first in primaryoutputs:
        outputdelay[first] = run(first)
        final_answer = max(final_answer,outputdelay[first])
    with open("longest_delay.txt", 'w') as Myfile:
        Myfile.write(f"{final_answer}")
else:
    inputdelays = {}
    gatedelays = {}
    nodedelay = {}
    desiredoutputdelay = {}
    nodeadj = {}
    primaryinputs = []
    primaryoutputs = []
    rd = sys.argv[4]
    with open(rd, 'r') as in_file:
        for line in in_file:
            text = line.strip()
            if not text:
                continue
            if text.startswith('//'):
                continue
            if text[0] == ' ':
                continue
            data = text.split()
            for i in range(len(data)):
                desiredoutputdelay[data[0]] = float(data[1])

    gd = sys.argv[3]
    with open(gd, 'r') as in1:
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
                gatedelays[data[0]] = float(data[1])
                
    ckt = sys.argv[2]
    with open(ckt, 'r') as in2:
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
                    inputdelays[data[i]] = INF
                elif data[0] == "PRIMARY_OUTPUTS":
                    primaryoutputs.append(data[i])
                elif data[0] == "INTERNAL_SIGNALS":
                    pass
                else:
                    if i == n - 1:
                        break
                    if data[i] not in nodeadj:
                        nodeadj[data[i]] = [[], INF]
                    nodeadj[data[i]][0].append(data[n - 1])
                    nodedelay[data[n - 1]] = gatedelays[data[0]]

    def run(node):
        if node in primaryoutputs:
            zero = desiredoutputdelay[node] - nodedelay[node]
            return zero
        elif nodeadj[node][1] != INF:
            return nodeadj[node][1]
        else:
            for child in nodeadj[node][0]:
                nodeadj[node][1] = min(nodeadj[node][1], run(child))
            nodeadj[node][1] -= nodedelay[node]
            return nodeadj[node][1]

    for node in primaryinputs:
        for child in nodeadj[node][0]:
            inputdelays[node] = min(inputdelays[node], run(child))

    with open("input_delays.txt", 'w') as Myfile2:
        for first in primaryinputs:
            Myfile2.write(f"{first} {inputdelays[first]}\n")
