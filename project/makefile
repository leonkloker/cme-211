CC = g++  
CFLAGS1 = -std=c++11 -Wall -Wconversion -Wextra -Wpedantic -c
CFLAGS2 = -O3 -std=c++11 -Wall -Wconversion -Wextra -Wpedantic

main: main.o CGSolver.o COO2CSR.o matvecops.o heat.o sparse.o
	$(CC) $(CFLAGS2) main.o CGSolver.o heat.o sparse.o COO2CSR.o matvecops.o -o main

main.o:	main.cpp
	$(CC) $(CFLAGS1) main.cpp

CGSolver.o: CGSolver.cpp CGSolver.hpp
	$(CC) $(CFLAGS1) CGSolver.cpp

COO2CSR.o: COO2CSR.cpp COO2CSR.hpp
	$(CC) $(CFLAGS1) COO2CSR.cpp

matvecops.o: matvecops.cpp matvecops.hpp
	$(CC) $(CFLAGS1) matvecops.cpp

sparse.o: sparse.cpp sparse.hpp
	$(CC) $(CFLAGS1) sparse.cpp

heat.o: heat.cpp heat.hpp
	$(CC) $(CFLAGS1) heat.cpp
	
clean:
	rm *.o main
