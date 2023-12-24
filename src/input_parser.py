from machine import Machine
from sim import Sim



class InputParser:
    def __init__(self):
        self.num_machine = 0
        self.num_cycle = 0
        self.op_wear = {"enhance":0,"reverse":0,"chop":0,"trim":0,"split":0}
        self.threshold = 0
        self.inputs = []
    
    def create_machine(self):
        self.machines = []
        self.leafs = []
        for i in range(self.num_machine):
            self.machines.append(Machine(i+1,self.threshold))
            self.leafs.append(i)

    def leaf_pop(self,num):
        if num in self.leafs:
            self.leafs.pop(num)

        
    def create_sim(self):
        self.sim = Sim(self.machines,self.inputs,self.leafs,self.num_cycle)

    def parse(self,file):
        f = open(file,'r')
        lines = f.readlines()
        self.num_machine = int(lines[0]) # num machines
        self.num_cycle = int(lines[1]) # num cycle
        op_wears = lines[2].split()
        op_keys = list(self.op_wear.keys())

        for idx,op_wear in enumerate(op_wears):
            self.op_wear[op_keys[idx]] = op_wear # operation wear factor
        self.threshold = int(lines[3]) # Maintenance threshold
        
        self.create_machine()



        for i in range(self.num_machine-1):
            tokens = lines[4+i].split()

            self.machines[int(tokens[0])-1].target = tokens[1]
            self.machines[int(tokens[1])-1].input_machines.append(tokens[0])
            self.leaf_pop(int(tokens[1]))

            self.machines[int(tokens[0])-1].operation = tokens[2] 
        count = 0
        for i in range(3+self.num_machine,3+self.num_machine+(len(self.leafs))):
            token = lines[i]
            self.inputs.append(token)
        self.create_sim()
        return self.sim