from mpi4py import MPI
import numpy as np
import sys


def main():
    # comm = MPI.COMM_WORLD
    # rank = comm.Get_rank()
    f = open(sys.argv[1],'r')
    lines = f.readlines()
    num_machine = int(lines[0])
    worker_comm = MPI.COMM_SELF.Spawn(sys.executable,args=["process.py",sys.argv[1],sys.argv[2],str(num_machine)],maxprocs=num_machine+2)

if __name__ == "__main__":
    main()