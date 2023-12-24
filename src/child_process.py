from mpi4py import MPI
from machine import Machine



comm = MPI.Comm.Get_parent() # MPI.Comm.Get_parent()
rank = comm.Get_rank()

commw = MPI.COMM_WORLD
rankw = commw.Get_rank()

print("rank and rankw : ",rank,rankw)


if rank == 0:
    pass

if rank != 0:
    print("hello I am not rank 0")
    maintenance = []
    machine = comm.recv(source=0)
    print(rank, " Received machine from mom.")
    

    if type(machine) != int:
        print(rank, " Starting process. ")
        machine.comm = comm
        machine.process()
    else:
        print(rank, " Hi I am logger------------------------------------")
        num_machine = machine - 1
        for i in range(num_machine):
            print(rank, " Logger reciving logs")
            log = commw.recv(source=i)
            if log != 0:
                maintenance.append(log)
        comm.send(maintenance,dest=0)

