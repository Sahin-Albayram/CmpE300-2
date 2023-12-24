from mpi4py import MPI


class Machine:
    def __init__(self,rank,threshold,op_wear,operation = None,comm = None,input_machines = [],target = None):
        self.input_machines = input_machines
        self.operation = operation
        self.op_wear = op_wear
        self.threshold = threshold
        self.rank = rank
        self.comm = comm
        self.target = target
        self.accumulated = 0

    def get_inputs(self,input=None):
        if input == None:
            self.inputs = []
            for machine in self.input_machines:
                self.input.append(self.comm.recv(source=machine.rank, tag=(10*machine.rank + self.rank)))
        else:
            self.inputs = [input]
    

    def output(self):
        self.comm.send(self.input,dest = self.target)

    def process(self):
        if len(self.inputs) == 0:
            self.get_inputs()
        self.output = ''
        for input in self.inputs:
            self.output += input

        if self.operation == "enhance":
            self.output = self.output[0] + self.output + self.output[-1]
            

        elif self.operation == "reverse":
            self.output = self.output[::-1]

        elif self.operation == "trim":
            self.output = self.output[1:-1] if len(self.output) > 2 else self.output

        elif self.operation == "chop":
            self.output = self.output[:-1] if len(self.output)> 1 else self.output
        
        elif self.operation == "split":
            self.output = self.output[:len(self.output)//2] if len(self.output)>1  else self.output
        
        self.accumulated += self.op_wear.get(self.operation)

        if self.target == None:
            self.comm.send(self.output,dest=0,tag=1)
        else:
            self.comm.send(self.output,dest=self.target)

        self.comm.send(self,dest=0,tag=0)

        return 0
        
