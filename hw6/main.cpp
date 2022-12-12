#include <iostream>
#include <stdio.h>

#include "image.hpp"

int main(){
    
    // create Image object and calculate sharpness of input picture
    std::string inputFile = "stanford.jpg";
    Image im(inputFile);
    unsigned int s = im.Sharpness();
    printf("Original image: %d ", s);

    // empty output buffer
    std::cout << std::flush;

    for (int kernel = 3; kernel <= 27; kernel = kernel + 4){

        // create Image object, blur and calculate sharpness
        im = Image(inputFile);
        im.BoxBlur(kernel);
        s = im.Sharpness();
        printf("BoxBlur(%d): %d ", kernel, s);

        // empty output buffer
        std::cout << std::flush;

        // save blurred image
        char str[20];
        sprintf(str, "BoxBlur%02d.jpg", kernel);
        im.Save(str);
    }

    return 0;

}
