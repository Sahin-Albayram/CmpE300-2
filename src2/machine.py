import copy

# this is a class for machines
class Machine:
    # it gets rank, threshold for maintenance, operation list, operation to process, input machines (machines that sends input to that machine)
    # and target machine (machine to send if it's not the root)
    def __init__(self,rank,threshold,op_wear,operation = None,input_machines = [],target = None):
        self.input_machines = copy.deepcopy(input_machines)
        self.operation = operation
        self.op_wear = op_wear
        self.threshold = threshold
        self.rank = rank
        self.target = target
        self.accumulated = 0
        self.inputs = []
        self.need_maint = False
        self.cost = 0
        self.cycle = 1


    def __getstate__(self):

        state = self.__dict__.copy()
        return state



    
    # this function checks accumulation as description desires, if threshold is lower equal to accumulation, it sets need_maint to observed from logs and calculates its cost
    def acc_check(self):
        if self.threshold <= self.accumulated:
            self.need_maint = True
            self.cost = (self.accumulated-self.threshold + 1)*(int(self.op_wear[self.operation]))

    # this is process for machine
    def process(self):
        self.output = ''
        # it first adds inputs
        for input in self.inputs:
            self.output += input
        
        # if there is no input, that means some error is occured
        if len(self.output) == 0:
            print("invalid input machine : ", self.rank, " broken")
            return 0
        
        # after addition it operates according to operation type
        if self.operation == "enhance":
            self.output = self.output[0] + self.output + self.output[-1]

        elif self.operation == "reverse":
            self.output = self.output[::-1]

        elif self.operation == "trim":
            self.output = self.output[1:-1] if len(self.output) > 2 else self.output

        elif self.operation == "chop":
            self.output = self.output[:-1] if len(self.output)> 1 else self.output
        
        elif self.operation == "split":
            if len(self.output) %2 == 0:
                self.output = self.output[:len(self.output)//2] if len(self.output)>1  else self.output
            else:
                self.output = self.output[:(len(self.output)//2)+1] if len(self.output)>1  else self.output
        
        # after it operates, it calculates its new accumulation then checks its accumulation. (if it's not the root machine)
        if self.rank != 1:

            self.accumulated += int(self.op_wear[self.operation])
            self.acc_check()
            
        # if self.target == None:
        #     print(self.rank, " Sending output to mom.")
        #     #self.comm.send(self.output,dest=0,tag=1)
        #     MPI.Comm.Get_parent().send(self.output,dest=0,tag=1)
        # else:
        #     print(self.rank, " Sending output to my brother : ", self.target)
        #     # self.commw.send(self.output,dest=self.target)
        #     MPI.COMM_WORLD.send(self.output,dest=self.target)



        #self.comm.send(self,dest=0,tag=0)
        return 0
        
