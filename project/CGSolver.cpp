#include <fstream>
#include <iostream>
#include <stdio.h>

#include "CGSolver.hpp"

int CGSolver(SparseMatrix &A, const std::vector<double> &b,
             std::vector<double> &x, double tol, std::string outputfile = "",
            unsigned int m = 0){
    /* This function solves a linear system Ax = b for a sparse matrix
    in place with the Conjugate Gradient method.
    
    Args:
        - SparseMatrix &A: Sparse matrix A in CSR format.
        - std::vector<double> &b: Right-hand side vector of the equation system.
        - std::vector<double> &x: Initial guess of the solution.
        - double tol: Tolerance for the L2 norm of the residual.
        - std::string outputfile: Outputfile to write the solution.
        - unsigned int m: Amount of stencils in x-direction.
        
    Returns:
        - int niter: Number of iterations needed for convergence.
    */  
    
    // calculate residual and its norm
    std::vector<double> Ap = A.MulVec(x);
    std::vector<double> r = vector_subtraction(b, Ap);
    double normr = l2_norm(r);
    double normr0 = normr;

    // initialize search direction p and declare needed variables
    std::vector<double> p = r;
    std::vector<double> temp;
    double alpha;
    double beta;
    double normr_old;
    unsigned int niter = 0;
    std::vector<double> boundary_val;

    // write the initial guess to a file if an outputfile is specified
    if (outputfile != ""){
        for (unsigned int i = 0; i < m; i++){
            boundary_val.push_back(b[i]);
        }
        for (unsigned int i = 0; i < m; i++){
            boundary_val.push_back(b[b.size()-m+i]);
        }
        WriteSolution(x, outputfile+"000.txt", m, boundary_val);
    }
    
    // iterate until tolerance is reached
    while ((niter < (unsigned int) x.size()) && ((normr / normr0) > tol)){
        niter++;

        // update solution x based on current search direction p
        Ap = A.MulVec(p);
        alpha = normr * normr / scalar_product(p, Ap);
        temp = scalar_multiplication(alpha, p);
        x = vector_addition(x, temp);

        // update residual and its norm accordingly
        temp = scalar_multiplication(alpha, Ap);
        r = vector_subtraction(r, temp);
        normr_old = normr;
        normr = l2_norm(r);

        // update the search direction p with the residual
        beta = (normr*normr) / (normr_old*normr_old);
        temp = scalar_multiplication(beta, p);
        p = vector_addition(r, temp);

        // write the current partial solution to a file if an outputfile is specified
        if ((outputfile != "") && (niter%10 == 0)){
            char file[40];
            sprintf(file, (outputfile+"%03d.txt").c_str(), niter);
            WriteSolution(x, file, m, boundary_val);
        }
    }

    // write the final solution to a file if an outputfile is specified
    if (outputfile != ""){
        char file[40];
        sprintf(file, (outputfile+"%03d.txt").c_str(), niter);
        WriteSolution(x, file, m, boundary_val);
    }

    // Output message if solver terminated because tolerance was reached
    if((normr / normr0) <= tol){
        std::cout << "SUCCESS: CG solver converged in " << niter << " iterations." << std::endl;
    }

    return niter;
}

void WriteSolution(const std::vector<double> &x, std::string outputfile,
            unsigned int m, const std::vector<double> &boundary_val){
    /* This writes the current solution vector x to the outputfile
    and pads with boundary values.
    
    Args:
        - std::vector<double> &x: Solution vector.
        - std::string outputfile: Outputfile.
        - unsigned int m: Amount of stencils in x-direction.
        - std::vector<double> &boundary_val: Vector containing the boundary values
        of the system.
    */

    // write bottom boundary values
    std::ofstream output(outputfile);
    for (unsigned int i = 0; i < m; i++){
        output << boundary_val[i] << " "; 
    }
    output << std::endl;

    // write bulk values the CG solver solved for
    for (unsigned int i = 0; i < x.size(); i++){
        if ((i%m == 0) && (i > 0)){
            output << std::endl;
        }
        output << x[i] << " ";     
    }
    output << std::endl;

    // write top boundary values
    for (unsigned int i = 0; i < m; i++){
        output << boundary_val[m+i] << " "; 
    }
    output << std::endl;
    
    output.close();
}
