from mpi4py import MPI
import sys
from input_parser import InputParser
from machine import Machine

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
machines = []
logger = int(sys.argv[3]) + 1 # machine + 1 , 44
log = [] # list for storing logs for maintenance 
accumulated = [0 for _ in range(int(sys.argv[3]))] # list for storing accumulation for machines 

requests = []

def create_machines(num,threshold,op_wear):
    for i in range(num):
        machines.append(Machine(i+1,threshold,op_wear)) #append created machines to the machine list (without appending the control room)
        

if rank == 0: # when this is called for control room

    maint_msg = []
    parser = InputParser()
    machines = parser.parse(sys.argv[1]) # parse the input file


    for i in range(len(parser.leafs)): 
            machines[parser.leafs[i]-1].inputs = parser.inputs[i] # attach machines inputs as parser inputs (because machines has indices that id+1 we use [i]-1)


    for cycle_no in range(1,parser.num_cycle): # loop as cycle number

        for rank in range(1,len(accumulated)+1): # storing all machines accumulations
            idx = rank-1
            machines[idx].accumulated = accumulated[idx]

        # for machine in machines:
        #     print(machine.rank , machine.operation, machine.input_machines, machine.target)
        comm.send(cycle_no,dest=logger) # send cycle number to the logger
    
        for i in range(1,parser.num_machine+1):
            comm.send((machines,cycle_no),dest=i) # send all machines to the machine



        log = comm.recv(source=logger) # get the log list from logger

        # print("logger has been read : ", log)

        


        result = comm.recv(source = parser.root[0],tag=1) # get the output from root 
 
        print(result) # print the output


        for i in range(1,logger):
            accumulated[i-1] = comm.recv(source=i) # get accumulateds from machines
        

        for machine in machines: # change their operations for the next cycle as requested
            if machine.operation == "trim":
                machine.operation = "reverse"

            elif machine.operation == "reverse":
                machine.operation = "trim"
                
            elif machine.operation == "split":
                machine.operation = "chop"

            elif machine.operation == "chop":
                machine.operation = "enhance"

            elif machine.operation == "enhance":
                machine.operation = "split"


    for i in range(1,parser.num_machine+1): # when cycles over, send -1 to machines to stop processing
        comm.send((machines,-1),dest=i)
    comm.send(-1,dest=logger) # when cycles over, send -1 to logger to stop processing
    print(log) # print the log

#-----------------------------------------------------

elif rank == logger: # logger 
    while(1):
        cycle_no = comm.recv(source=0) # get cycle number from control room
        if cycle_no == -1: # if it is -1, it means cycles are over break it
            break
        for i in range(1,logger): 
            msg = comm.recv(source=i) # get maintanance messages from machines
            if msg != None:
                log.append(msg) # if message is not null append that to the log list

        comm.send(log,dest=0) # send the list to the control room


#-----------------------------------------------------


else: # Kids right here 
    while(1):
        machines,cycle_no = comm.recv(source=0) # get machines and cycle number from control room
        if(cycle_no == -1): # if it gets cycle number as -1, stop the process
            break

        msg = None
        machine = machines[rank-1] #current machine is processes rank - 1 rank0 -> control, rank1 -> root(machine[0]), rank[i] -> machine[i-1]




        if len(machine.inputs) == 0: # if it has no input (which means it's not leaf so it has input machines)
            input_machines = machine.input_machines 
            for id in input_machines:
                machine.inputs.append(comm.recv(source=id)) # it wait for input machine's response


        
        machine.process() # process machine with the operation


        if machine.need_maint: # if it needs a maintance, it prepares the message and reset accumulated
            msg = str(machine.rank) + "-"+ str(machine.cost) + "-" + str(cycle_no)
            machine.accumulated = 0
            machine.need_maint = False


        if machine.target == None: # if it is root send output to the control room
            comm.send(machine.output,dest=0,tag=1) 
        else: # else send its output to its target
            comm.send(machine.output,dest=machine.target)
        
        comm.send(msg,dest=logger) # send message to the logger

        comm.send(machine.accumulated,dest= 0) # send current accumulation to the control room



MPI.Finalize()