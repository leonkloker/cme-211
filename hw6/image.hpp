#pragma once

#include "hw6.hpp"

class Image {
    private:
        std::string inputFile;

        boost::multi_array<unsigned char, 2> imageOriginal;
        boost::multi_array<unsigned char, 2> imageEdited;

        unsigned int Index(unsigned int size, int index);

    public:
        Image(std::string filename);

        void Save(std::string outputFile);
        void Save();

        void Convolution(boost::multi_array<unsigned char,2>& input,
                     boost::multi_array<unsigned char,2>& output,
                     boost::multi_array<float,2>& kernel);

        void BoxBlur(int kernelSize);

        unsigned int Sharpness();
};
