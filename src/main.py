from mpi4py import MPI
import numpy as np
from input_parser import InputParser
import sys

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    parser = InputParser()
    sim = parser.parse(sys.argv[1])
    

    if rank == 0:
        pass


if __name__ == "__main__":
    main()