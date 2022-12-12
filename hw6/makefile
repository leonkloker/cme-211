
main: main.o image.o hw6.o
	g++ -std=c++11 -Wall -Wconversion -Wextra -Wpedantic main.o image.o hw6.o -ljpeg -o main

main.o:	main.cpp
	g++ -std=c++11 -Wall -Wconversion -Wextra -Wpedantic -c main.cpp

message.o: image.cpp image.hpp
	g++ -std=c++11 -Wall -Wconversion -Wextra -Wpedantic -c image.cpp

hw6.o: hw6.cpp hw6.hpp
	g++ -std=c++11 -Wall -Wconversion -Wextra -Wpedantic -c hw6.cpp
	
clean:
	rm *.o main
