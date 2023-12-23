from mpi4py import MPI


class Machine:
    def __init__(self,rank,operation = None,comm = None,input_machines = [],target = None):
        self.input_machines = input_machines
        self.type = operation
        self.rank = rank
        self.odd = True if rank%2 == 1 else False
        self.comm = comm
        self.target = target

    def get_inputs(self,input=None):
        if input == None:
            self.inputs = []
            for machine in self.input_machines:
                self.input.append(self.comm.recv(source=machine.rank, tag=(10*machine.rank + self.rank)))
        else:
            self.inputs = [input]
    

    def output(self):
        self.comm.send(self.input,dest = self.target,tag = (10*self.rank + self.target.rank))

    def process(self):
        self.input = ''
        for input in self.inputs:
            self.input += input

        if self.operation == "enhance":
            self.input = self.input[0] + self.input + self.input[-1]

        elif self.operation == "reverse":
            self.input = self.input[::-1]

        elif self.operation == "trim":
            self.input = self.input[1:-1] if len(self.input) > 2 else self.input

        elif self.operation == "chop":
            self.input = self.input[:-1] if len(self.input)> 1 else self.input
        
        elif self.operation == "split":
            self.input = self.input[:len(self.input)//2] if len(self.input)>1  else self.input
        
        
