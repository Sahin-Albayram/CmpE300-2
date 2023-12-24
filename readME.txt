to use mpi4y you need to do
in MAC first:
pip3 install mpi4py 
if it doesn't work:
brew install mpich
export MPICC=/path/to/mpicc
export MPI_ROOT=/path/to/mpi
pip3 install mpi4py

then:
mpiexec -n 1 python main.py input.txt output.txt

We didn't try to run this code in Windows, installing mpi4py and mpich for windows, then add mpi4py to environmental path then command (will work hopefully):
mpiexec -n 1 python main.py input.txt output.txt