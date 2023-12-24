from mpi4py import MPI


class Machine:
    def __init__(self,rank,threshold,op_wear,operation = None,input_machines = [],target = None):
        self.input_machines = input_machines
        self.operation = operation
        self.op_wear = op_wear
        self.threshold = threshold
        self.rank = rank
        self.target = target
        self.accumulated = 0
        self.inputs = []


    def __getstate__(self):

        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):

        self.__dict__.update(state)

    def get_inputs(self,input=None):
        if input == None:
            self.inputs = []
            for machine in self.input_machines:
                print(self.rank, " getting input from my brother : ", machine)

                self.inputs.append(MPI.COMM_WORLD.recv(source=machine))
                #self.inputs.append(self.commw.recv(source=machine))
        else:
            self.inputs = [input]
    

    def output(self):
        # self.commw.send(self.input,dest = self.target)
        MPI.COMM_WORLD.send(self.input,dest = self.target)

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
        
        self.accumulated += int(self.op_wear[self.operation])

        if self.target == None:
            print(self.rank, " Sending output to mom.")
            #self.comm.send(self.output,dest=0,tag=1)
            MPI.Comm.Get_parent().send(self.output,dest=0,tag=1)
        else:
            print(self.rank, " Sending output to my brother : ", self.target)
            # self.commw.send(self.output,dest=self.target)
            MPI.COMM_WORLD.send(self.output,dest=self.target)



        #self.comm.send(self,dest=0,tag=0)
        return 0
        
