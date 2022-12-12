#include "image.hpp"

Image::Image(std::string filename){
    /* Constructor of the image class.
    
    Args: 
        - std::string filename: Name of the input image file.
        
    */

    this->inputFile = filename;
    ReadGrayscaleJPEG(this->inputFile, this->imageOriginal);
    this->imageEdited.resize(boost::extents[this->imageOriginal.shape()[0]][this->imageOriginal.shape()[1]]);
    this->imageEdited = this->imageOriginal;
}

void Image::Save(std::string filename){
    /* This function saves the edited image to the filename.
    
    Args:
        - std::string filename: Name of the output file.
        
    */

    WriteGrayscaleJPEG(filename, this->imageEdited);
}

void Image::Save(){
    /* This function overwrites the input image with the edited image.
    
    */

    WriteGrayscaleJPEG(this->inputFile, this->imageEdited);
}

void Image::Convolution(boost::multi_array<unsigned char,2>& input,
                    boost::multi_array<unsigned char,2>& output,
                    boost::multi_array<float,2>& kernel){
    /* This function performs a padded convolution on the input with the
    specified kernel and saves the result in output.
    
    Args:
        - boost::multi_array<unsigned char,2>& input: Input image.
        - boost::multi_array<unsigned char,2>& output: Output image.
        - boost::multi_array<float,2>& kernel: Convolution kernel.
        
    */

    unsigned int n_x = input.shape()[0];
    unsigned int n_y = input.shape()[1];

    // ensure that output has the same size as input
    output.resize(boost::extents[n_x][n_y]);

    // calculate offsets for the convolution
    int offset_x = (int) (-kernel.shape()[0] / 2);
    int offset_y = (int) (-kernel.shape()[1] / 2);

    // iterate over all pixel positions in the output picture
    for (int i = 0; i < n_x; i++){
        for (int j = 0; j < n_y; j++){
            float value = 0;

            // iterate over all positions in the kernel
            for (int k = 0; k < kernel.shape()[0]; k++){
                for (int l = 0; l < kernel.shape()[1]; l++){
                    value += kernel[k][l] * input[this->Index(n_x, i+offset_x+k)][this->Index(n_y, j+offset_y+l)];
                }
            }

            // handle overflow of unsigned chars
            if (value < 0){
                output[i][j] = 0;
            }else if (value > 255){
                output[i][j] = 255;
            }else{
                output[i][j] = (unsigned char) value;
            }
        }
    }
}

unsigned int Image::Index(unsigned int size, int index){
    /* This function gives the index of the value in the input image that
    should be accessed for a given real index. This is done to handle padding.
    
    Args:
        - unsigned int size: Size of the input image.
        - int index: Index.
        
    */

    if (index < 0){
        return 0;
    }

    if (index >= size){
        return size - 1;
    }

    return index;
}

void Image::BoxBlur(int kernelSize){
    /* This function performs a box blur on the image.
    
    Args:
        - int kernelSize: Size of the kernel to be used for the blurring.
        
    */

    // initialize homogeneous kernel
    boost::multi_array<float,2> kernel(boost::extents[kernelSize][kernelSize]);
    std::fill_n(kernel.data(), kernel.num_elements(), (float) 1/kernel.num_elements());

    // run the convolution and save the result
    boost::multi_array<unsigned char, 2> imageOutput;
    this->Convolution(this->imageEdited, imageOutput, kernel);
    this->imageEdited = imageOutput;
}

unsigned int Image::Sharpness(){
    /* This function calculates the sharpness of the image with a 2d Laplace
    kernel.
        
    */

    unsigned int sharpness = 0;

    // initialize kernel
    boost::multi_array<float, 2> kernel(boost::extents[3][3]);
    boost::multi_array<unsigned char, 2> imageOutput;
    std::fill_n(kernel.data(), kernel.num_elements(), 0);
    kernel[0][1] = 1;
    kernel[1][0] = 1;
    kernel[1][2] = 1;
    kernel[2][1] = 1;
    kernel[1][1] = -4;

    // run convolution
    this->Convolution(this->imageEdited, imageOutput, kernel);

    // get maximum value in output image
    sharpness = (unsigned int) *std::max_element(imageOutput.data(), imageOutput.data() + imageOutput.num_elements());

    return sharpness;
}
