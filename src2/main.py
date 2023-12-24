#Egecan Serbester 2019400231
#Ömer Şahin Albayram 2021400303
#group no : 33


from mpi4py import MPI
import numpy as np
import sys


def main():
    # comm = MPI.COMM_WORLD
    # rank = comm.Get_rank()
    f = open(sys.argv[1],'r') #open file for read
    lines = f.readlines()  # read lines
    num_machine = int(lines[0]) #get number of machine
    # spawn as number of machines + 2 process (1 for control room, 1 for logger)
    worker_comm = MPI.COMM_SELF.Spawn(sys.executable,args=["process.py",sys.argv[1],sys.argv[2],str(num_machine)],maxprocs=num_machine+2)

if __name__ == "__main__":
    main()