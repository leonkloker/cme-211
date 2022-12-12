#include "matvecops.hpp"

std::vector<double> csr_matrix_vector_muliplication(const std::vector<double> &val, 
    const std::vector<int> &row_ptr, const std::vector<int> &col_idx,
    const std::vector<double> &b){
    /*This function performs a matrix-vector multiplication where the matrix
    is given by val, row_ptr and col_idx in the CSR format. 
    
    Args:
        - std::vector<double> &val: Values of the CSR format.
        - std::vector<int> &row_ptr: Row indices of the CSR format.
        - std::vector<int> &col_idx: Column indices of the CSR format.
        - std::vector<double> &b: Vector to be multiplied.
        
    Returns:
        - std::vector<double> res: Result of the matrix-vector multiplication.      
    */

    int n = (int) b.size();
    std::vector<double> res(n, 0.);

    for (int i = 0; i < (int) row_ptr.size()-1; i++){
        for(int j = row_ptr[i]; j < row_ptr[i+1]; j++){
            res[i] += val[j] * b[col_idx[j]];
        }
               
    }
    return res;
}

std::vector<double> vector_addition(const std::vector<double> &v1,
    const std::vector<double> &v2){
    /*This function performs an elementwise addition of two vectors.
    
    Args:
        - std::vector<double> &v1: First vector.
        - std::vector<int> &v2: Second vector.
        
    Returns:
        - std::vector<double> res: Result of the addition.     
    */

    std::vector<double> res(v1.size(), 0.);
    for (unsigned int i = 0; i < v1.size(); i++){
        res[i] = v1[i] + v2[i];
    }
    return res;
}

std::vector<double> vector_subtraction(const std::vector<double> &v1,
    const std::vector<double> &v2){
    /*This function performs an elementwise subtraction of two vectors.
    
    Args:
        - std::vector<double> &v1: First vector.
        - std::vector<int> &v2: Vector to be subtracted.
        
    Returns:
        - std::vector<double> res: Result of the subtraction.   
    */

    std::vector<double> res(v1.size(), 0.);
    for (unsigned int i = 0; i < v1.size(); i++){
        res[i] = v1[i] - v2[i];
    }
    return res;
}

std::vector<double> scalar_multiplication(double a, const std::vector<double> &v){
    /*This function performs a scalar times vector multiplication.
    
    Args:
        - double a: Scalar.
        - std::vector<double> &v: Vector to be multiplied by scalar.
        
    Returns:
        - std::vector<double> res: Result of the scalar multiplication.     
    */

    std::vector<double> res(v.size(), 0.);
    for (unsigned int i = 0; i < v.size(); i++){
        res[i] = v[i] * a;
    }
    return res;
}

double l2_norm(const std::vector<double> &v){
    /*This function calculates the L2 norm of a vector.
    
    Args:
        - std::vector<double> &v: Vector.
        
    Returns:
        - double norm: L2 norm of the vector.
    */

    double norm = scalar_product(v, v);
    return std::sqrt(norm);
}

double scalar_product(const std::vector<double> &v1,
    const std::vector<double> &v2){
    /*This function calculates the L2 inner product of two vectors.
    
    Args:
        - std::vector<double> &v1: First vector.
        - std::vector<double> &v2: Second vector.
        
    Returns:
        - double sum: Inner product.
    */

    double sum = 0;
    for (unsigned int i = 0; i < v1.size(); i++){
        sum += v1[i] * v2[i];
    }
    return sum;
}
