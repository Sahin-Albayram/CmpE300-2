from mpi4py import MPI
import sys
from input_parser import InputParser
from machine import Machine

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
machines = []
logger = int(sys.argv[3]) + 1 # machine + 1 , 44
log = []
accumulated = [0 for _ in range(int(sys.argv[3]))]

requests = []

def create_machines(num,threshold,op_wear):
    for i in range(num):
        machines.append(Machine(i+1,threshold,op_wear))
        

if rank == 0:

    maint_msg = []
    parser = InputParser()
    machines = parser.parse(sys.argv[1])


    for i in range(len(parser.leafs)):
            machines[parser.leafs[i]-1].inputs = parser.inputs[i]


    for cycle_no in range(1,30):

        for rank in range(1,len(accumulated)+1):
            idx = rank-1
            machines[idx].accumulated = accumulated[idx]

        # for machine in machines:
        #     print(machine.rank , machine.operation, machine.input_machines, machine.target)
        comm.send(cycle_no,dest=logger)
    
        for i in range(1,parser.num_machine+1):
            comm.send((machines,cycle_no),dest=i)



        log = comm.recv(source=logger)

        # print("logger has been read : ", log)

        


        result = comm.recv(source = parser.root[0],tag=1)

        print(result)


        for i in range(1,logger):
            accumulated[i-1] = comm.recv(source=i)
        

        for machine in machines:
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


    for i in range(1,parser.num_machine+1):
        comm.send((machines,-1),dest=i)
    comm.send(-1,dest=logger)
    print(log)
#-----------------------------------------------------


elif rank == logger: # logger 
    while(1):
        cycle_no = comm.recv(source=0)
        if cycle_no == -1:
            break
        for i in range(1,logger):
            msg = comm.recv(source=i)
            if msg != None:
                log.append(msg)

        comm.send(log,dest=0)


#-----------------------------------------------------


else: # Kids right here 
    while(1):
        machines,cycle_no = comm.recv(source=0)
        if(cycle_no == -1):
            break

        msg = None
        machine = machines[rank-1]




        if len(machine.inputs) == 0:
            input_machines = machine.input_machines
            for id in input_machines:
                machine.inputs.append(comm.recv(source=id))


        
        machine.process()


        if machine.need_maint:
            msg = str(machine.rank) + "-"+ str(machine.cost) + "-" + str(cycle_no)
            machine.accumulated = 0
            machine.need_maint = False


        if machine.target == None:
            comm.send(machine.output,dest=0,tag=1)
        else:
            comm.send(machine.output,dest=machine.target)
        
        comm.send(msg,dest=logger)

        comm.send(machine.accumulated,dest= 0)



MPI.Finalize()