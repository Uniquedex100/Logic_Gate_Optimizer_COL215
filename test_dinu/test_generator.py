import random

# Define the gate names and their corresponding gate types
gate_names = [
    "NAND2_1", "NAND2_2", "NAND2_3",
    "AND2_1", "AND2_2", "AND2_3",
    "NOR2_1", "NOR2_2", "NOR2_3",
    "OR2_1", "OR2_2", "OR2_3",
    "INV_1", "INV_2", "INV_3"
]
gate_types = [
    "NAND2", "NAND2", "NAND2",
    "AND2", "AND2", "AND2",
    "NOR2", "NOR2", "NOR2",
    "OR2", "OR2", "OR2",
    "INV", "INV", "INV"
]
low = 9
high = 10
n = random.choice(range(low,high))
print("n = ",n)
matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(0, n):
        if(i==j) : 
            matrix[i][j] = 0
        else : 
            matrix[j][i] = matrix[i][j]
for row in matrix:
    print(row)

# not necessarily binary gates : 
forwardedge = {}
ismapped = {}
backwardedge = {}
for i in range(n) : 
    backwardedge[i] = []
for i in range(n) : 
    forwardedge[i] = []
    for j in range(i,n) : 
        if matrix[i][j] == 1:
            forwardedge[i] . append(j)
            backwardedge[j]. append(i)
            ismapped[j] = 1
print(forwardedge)
print(backwardedge)

inputset = []
outputset = []
internalset = []
for node in forwardedge : 
    if ((len(forwardedge[node]) == 0) and (node not in ismapped)) : #handle stray nodes
        matrix[1][node] = 1
        forwardedge[1].append(node)
        backwardedge[node].append(i)
        ismapped[node] = 1
    if (len(forwardedge[node]) == 0) : 
        outputset.append(node)
    elif node not in ismapped : 
        inputset.append(node)
    else :
        internalset.append(node)
    

i = len(inputset)        
print("i = ",i)
o = len(outputset)
print("o = ",o)
print("input set : ",inputset)
print("output set : ",outputset)
internalset = list(set(range(n)) - set(inputset) - set(outputset))
print("internal set : ",internalset)

def generate_random_strings(count):
    strings = []
    for _ in range(count):
        while True:
            # Generate a random string of length 5
            random_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(5))
            if random_string not in strings:
                strings.append(random_string)
                break
    return strings

# Create mapping dictionaries
inputmap = {element: string for element, string in zip(inputset, generate_random_strings(i))}
outputmap = {element: string for element, string in zip(outputset, generate_random_strings(o))}
internalmap = {element: string for element, string in zip(internalset, generate_random_strings(len(internalset)))}

# Create the circuit description
primary_inputs = []
primary_outputs = []
internal_signals = []
for m in inputmap : 
    primary_inputs.append(inputmap[m])
for m in outputmap : 
    primary_outputs.append(outputmap[m])
for m in internalmap : 
    internal_signals.append(internalmap[m])

circuit = "PRIMARY_INPUTS " + " ".join(primary_inputs) + "\n"
circuit += "PRIMARY_OUTPUTS " + " ".join(primary_outputs) + "\n"
circuit += "INTERNAL_SIGNALS " + " ".join(internal_signals) + "\n"

# Add gate descriptions
tobewritten = inputset + outputset
for i in range(len(tobewritten)):
    gate_type = random.choice(gate_types)
    circuit += f"{gate_type}  \n"

# Create random gate delay values
gate_delays = []
for i in range(len(gate_names)):
    gate_name = gate_names[i]
    gate_type = gate_types[i]
    gate_delay = round(random.uniform(2, 20), 2)  # Random delay between 2 and 20
    gate_area = round(random.uniform(2, 20), 2)  # Random delay between 2 and 20
    gate_delays.append(f"{gate_name} {gate_type} {gate_delay} {gate_area}")

# Set the delay constraint
delayconstraint = round(random.uniform(1, 10), 2)  # Random constraint between 1 and 10

# Write the data to files
with open("test_dinu/circuit.txt", 'w') as circuit_file:
    circuit_file.write(circuit)

with open("test_dinu/delay_constraint.txt", 'w') as constraint_file:
    constraint_file.write(str(delayconstraint))

with open("test_dinu/gate_delays.txt", 'w') as gate_delay_file:
    gate_delay_file.write("\n".join(gate_delays))


# with open("test_dinu/circuit.txt", 'w') as Myfile:
#             Myfile.write(f"{minarea}")
# with open("test_dinu/delay_constraint.txt", 'w') as Myfile:
#             Myfile.write(f"{delayconstraint}")
# with open("test_dinu/gate_delays.txt", 'w') as Myfile:
#             Myfile.write(f"{minarea}")
# with open("test_dinu/longest_delay.txt", 'w') as Myfile:
#             Myfile.write(f"{minarea}")
# with open("test_dinu/minimum_area.txt", 'w') as Myfile:
#             Myfile.write(f"{minarea}")