#include <cmath>
#include <fstream>

#include "heat.hpp"


int HeatEquation2D::Setup(std::string inputfile){
    /* This function initializes the matrix A and load vector b
    for the linear system describing the steady-state heat equation
    with the given parameters specified in the inputfile.
    
    Args:
        - std::string inputfile: File containing width, height, h, tc and th.
        
    Returns:
        - int: 0 if execution was successfull.
    */  

    // get parameters from file
    std::ifstream input(inputfile);
    input >> this->width >> this->height >> this->h;
    input >> this->tc >> this->th;
    input.close();

    // stencils in x and y direction
    this->m = (int) (this->width/this->h);
    this->n = (int) (this->height/this->h - 1);

    // initialize load vector
    for (int i = 0; i < this->m * this->n; i++){
        this->b.push_back(0);
    }

    // initialize matrix A
    for (int j = 0; j < n ; j++){
        for (int i = 0; i < m; i++){

            // bulk stencil, no boundaries
            if ((j != 0) && (j != n-1)){
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i, j), 4);
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i, j-1), -1);
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i, j+1), -1);
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i-1, j), -1);
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i+1, j), -1);

            // bottom boundary stencil
            }else if(j == 0){
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i, j), 4);
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i, j+1), -1);
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i-1, j), -1);
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i+1, j), -1);
                this->b[j*m+i] = this->LowerBoundary(this->width * i / this->m);

            // top boundary stencil
            }else{
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i, j), 4);
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i, j-1), -1);
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i-1, j), -1);
                this->A.AddEntry(j*m+i, this->PeriodicIndex(i+1, j), -1);
                this->b[j*m+i] = this->UpperBoundary();
            }
        }
    }
    return 0;
}

int HeatEquation2D::Solve(std::string soln_prefix){
    /* This function solves the linear system Ax = b arising
    from the steady-state heat equation via CG and writes
    the iterative solution to soln_prefix every 10 iterations.
    
    Args:
        - std::string soln_prefix: Prefix of solution files.

    Returns:
        - int: 0 for successfull execution.
    */  

    this->A.ConvertToCSR();

    // initial solution guess
    std::vector<double> x(this->m * this->n, 0.);

    double tol = 0.00001;

    // Call solver
    CGSolver(this->A, this->b, x, tol, soln_prefix, this->m);
    
    return 0;
}

int HeatEquation2D::PeriodicIndex(int i, int j){
    /* This function wraps the x index around the domain
    to handle periodic boundary conditions.
    
    Args:
        - int i: x index.
        - int j: y index.
        
    Returns:
        - int: Wrapped index.
    */  

    // if trying to access left boundary
    if (i == -1){
        return j * this->m + (this->m - 1);

    // if trying to access right boundary
    }else if(i == m){
        return j * this->m;

    // if in the middle
    }else{
        return j * this->m + i;
    }
}

double HeatEquation2D::LowerBoundary(double x){
    /* This function defines the bottom boundary
    heat distribution.
    
    Args:
        - double x: x position of heat field.
        
    Returns:
        - double: Heat at specified position.
    */  

    return -this->tc * (std::exp(-10 * std::pow(x - this->width / 2., 2)) - 2);
}

double HeatEquation2D::UpperBoundary(){
    /* This function defines the top boundary
    heat distribution.
        
    Returns:
        - double: Heat at top boundary.
    */ 

    return this->th;
}
