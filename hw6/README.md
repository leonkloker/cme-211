The Image class can be used to load a greyscale image from a file. The sharpness
of the loaded image can be calculated by performing a convolution with a Laplace
kernel on the input image and finding the largest value in the output image.
Moreover, the image can be blurred by performing a convolution with a 
homogeneous kernel of arbitrary size. The convolution method can be used to run
convolutions with arbitrary kernels. The image can then be saved to a new file
or the input image can be overwritten.

The main.cpp file loads the stanford.jpg greyscale image from the file and
calculates its sharpness. Furthermore, box blur operations with increasing
kernel size are performed and the resulting output image is saved to a file.
The sharpness of the blurred images is written to the command line.

$ make
g++ -std=c++11 -Wall -Wconversion -Wextra -Wpedantic -c main.cpp
g++    -c -o image.o image.cpp
g++ -std=c++11 -Wall -Wconversion -Wextra -Wpedantic -c hw6.cpp
g++ -std=c++11 -Wall -Wconversion -Wextra -Wpedantic main.o image.o hw6.o -ljpeg -o main

$ ./main
Original image: 255 BoxBlur(3): 139 BoxBlur(7): 44 BoxBlur(11): 27 BoxBlur(15):
21 BoxBlur(19): 16 BoxBlur(23): 11 BoxBlur(27): 9
