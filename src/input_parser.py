from machine import Machine
from sim import Sim



class InputParser:
    def __init__(self):
        self.num_machine = 0
        self.num_cycle = 0
        self.op_wear = {"enhance":0,"reverse":0,"chop":0,"trim":0,"split":0}
        self.maintenance = 0
    
    def create_machine(self):
        self.machines = []
        for i in range(self.num_machine):
            self.machines.append(Machine(i+1))


    def create_sim(self):
        pass

    def parse(self,file):
        f = open(file,'r')
        lines = f.readlines()
        self.num_machine = int(lines[0]) # num machines
        self.num_cycle = int(lines[1]) # num cycle
        op_wears = lines[2].split()
        op_keys = list(self.op_wear.keys())

        for idx,op_wear in enumerate(op_wears):
            self.op_wear[op_keys[idx]] = op_wear # operation wear factor
        self.maintenance = int(lines[3]) # Maintenance 
        
        self.create_machine()



        for i in range(self.num_machine-1):
            tokens = lines[4+i].split()
            self.machines[int(tokens[0])-1].target = tokens[1]
            self.machines[int(tokens[0])-1].operation = tokens[2] 