from mpi4py import MPI
import numpy as np
from machine import Machine
import sys

class Sim:
    def __init__(self,machines,inputs,leafs,num_cycles,root):
        self.machines = machines
        inputs.sort()
        leafs.sort()
        self.inputs = inputs
        self.leafs = leafs
        self.num_cycles = num_cycles
        self.root = root
        self.results = []
        self.maintenance = []

    def put_inputs(self):
        if len(self.leafs) != len(self.inputs):
            print("number of leafs and inputs are different")
            return 0
        else:
            for i in range(len(self.leafs)):
                print("machine : ", self.machines[self.leafs[i]-1].rank, " leaf : ", self.leafs[i], " input : " , self.inputs[i])
                self.machines[self.leafs[i]-1].inputs.append(self.inputs[i])

    def arrange_operations(self):
        for machine in self.machines:
            if machine.operation == "trim":
                machine.operation = "reverse"

            if machine.operation == "reverse":
                machine.operation = "trim"
                
            if machine.operation == "split":
                machine.operation = "chop"

            if machine.operation == "chop":
                machine.operation = "enhance"

            if machine.operation == "enhance":
                machine.operation = "split"

    def print_results(self):
        for result in self.results:
            print(result)
        for log in self.maintenance:
            print(log)

    
    def start_sim(self):
        
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        rank_logger = len(self.machines)+1
        if rank != 0:
            return 0
        worker_comm = MPI.COMM_SELF.Spawn(sys.executable,args=["child_process.py"],maxprocs=len(self.machines)+2,root=0)

        
        if worker_comm.Get_remote_size() != len(self.machines)+2:
            print("creating process step failed ", worker_comm.Get_remote_size(), " " ,len(self.machines)+2)
            return 0
        
        

        for i in range(self.num_cycles):
            self.put_inputs()

            for i in range(1,len(self.machines)+1):
                worker_comm.send(self.machines[i-1],dest=i)
            worker_comm.send(rank_logger,dest=rank_logger)


            result = worker_comm.recv(source=self.root,tag=1)
            self.results.append(result)


            maintenance = worker_comm.recv(source = rank_logger)
            self.maintenance.append(maintenance)

            self.arrange_operations()


