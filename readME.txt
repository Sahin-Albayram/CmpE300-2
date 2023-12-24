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

Notes:
You might have to change your /etc/hosts file to run code. You should add a line with your hostname as your localhost ip, for example
"127.0.0.1 locahost" is in your /etc/hosts file and your hostname is "IamHost" then you should add
"127.0.0.1 IamHost" 
this might fix if you get "Fatal error in MPI_Init_thread: Invalid group, error stack:" error