from mpi4py import MPI
from machine import Machine

comm = MPI.Comm.Get_parent()
rank = comm.Get_rank()

machine = comm.recv(source=0)

machine.process()

