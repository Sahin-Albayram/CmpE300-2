#Egecan Serbester 2019400231
#Ömer Şahin Albayram 2021400303
#group no : 33


from machine import Machine

# this class is for parsing the input from file
class InputParser:
    # initialize num of machines, cycles, threshold and inputs, and the cost of each operation
    def __init__(self):
        self.num_machine = 0
        self.num_cycle = 0 
        self.op_wear = {"enhance":0,"reverse":0,"chop":0,"trim":0,"split":0}
        self.threshold = 0
        self.inputs = []
    
    def create_machine(self):
        self.machines = [] # this is for machines (1,num_machine+1)
        self.leafs = [] # this is for leafs who takes input
        self.root = [] # this is for root who communicates with control room
        for i in range(self.num_machine):
            self.machines.append(Machine(i+1,self.threshold,self.op_wear)) # appends machines into machines list
            self.leafs.append(i+1) # append all indices of machines into leaf
            self.root.append(i+1)  # append all indices of machines into root

    def leaf_pop(self,num): # pop an index of machine from leaf (this is called when we understand it's not leaf)
        if num in self.leafs:
            self.leafs.remove(num)

    def root_pop(self,num): # pop an index of machine from root (this is called when we understand it's not leaf)
        if num in self.root:
            self.root.remove(num)
    

    def parse(self,file): # this parses the file
        f = open(file,'r')
        lines = f.readlines()
        self.num_machine = int(lines[0]) # num machines
        self.num_cycle = int(lines[1]) # num cycle
        op_wears = lines[2].split()
        op_keys = list(self.op_wear.keys()) # this matches operation costs with op_wear dictionary

        for idx,op_wear in enumerate(op_wears):
            self.op_wear[op_keys[idx]] = op_wear # operation wear factor
        self.threshold = int(lines[3]) # Maintenance threshold
        
        self.create_machine()



        for i in range(self.num_machine-1):
            tokens = lines[4+i].split() 

            self.machines[int(tokens[0])-1].target = int(tokens[1]) #tokens[0]-1 because input starts with machine 2, and it is in index 1, because the root machine is in index 1.
            self.root_pop(int(tokens[0])) # because root couldn't in input, we pop the root (this is for cases when root's id's is not 1 if it happens)


            self.machines[int(tokens[1])-1].input_machines.append(int(tokens[0])) #int(tokens[1])-1 because its index is -1 of its id, appends inputs of parent machines id of current machine tokens[0]
            self.leaf_pop(int(tokens[1])) # because it has some input machines, it can't be a leaf therefore we pop it from that list

            self.machines[int(tokens[0])-1].operation = tokens[2] # assign the initial operation to
        count = 0
        for i in range(3+self.num_machine,3+self.num_machine+(len(self.leafs))): # for other lines, assign inputs to corresponding leaf nodes
            token = lines[i].rstrip()
            self.inputs.append(token)
        return self.machines