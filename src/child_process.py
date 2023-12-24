from mpi4py import MPI
from machine import Machine

comm = MPI.Comm.Get_parent()
rank = comm.Get_rank()

maintenance = []
machine = comm.recv(source=0)

if type(machine) != int:
    machine.process()
else:
    num_machine = machine - 1
    for i in range(num_machine):
        log = comm.recv(source=i)
        if log == 0:
            continue
        else:
            maintenance.append(log)
    comm.send(maintenance,dest=0)
