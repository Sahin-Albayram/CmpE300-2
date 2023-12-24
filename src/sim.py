from mpi4py import MPI
import numpy as np
from machine import Machine
import sys

class Sim:
    def __init__(self,machines,inputs,leafs,cycles,root):
        self.machines = machines
        self.inputs = inputs
        self.leafs = leafs
        self.cycles = cycles
        self.root = root

    def create_process(self):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        if rank != 0:
            return 0
        worker_comm = MPI.COMM_SELF.Spawn(sys.executable,args=["child_process.py"],maxprocs=len(self.machines))



        for i in range(self.cycles):
            

            for i in range(1,len(self.machines)+1):
                worker_comm.send(self.machines[i-1],dest=i)
            
            for i in range(1,len(self.machines)+1):
                self.machines[i-1] = worker_comm.recv(source=i)

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

