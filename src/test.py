from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank ==0:
    print(comm.recv(source=1))
if rank == 1:
    comm.send("hello",dest=0)