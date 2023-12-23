from mpi4py import MPI
import numpy as np
from machine import Machine


class Sim:
    def __init__(self,machines,connections,inputs,leafs):
        self.machines = machines
        self.conn = connections
        self.inputs = inputs
        self.leafs = leafs
        
