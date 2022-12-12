#include "COO2CSR.hpp"
#include "matvecops.hpp"
#include "sparse.hpp"

void SparseMatrix::AddEntry(int i, int j, double val){
    /* This function adds an entry to the sparse matrix.
    
    Args:
        - int i: Row index.
        - int j: Column index.
        - double val: Value to be added.
    */ 

    this->a.push_back(val);
    this->i_idx.push_back(i);
    this->j_idx.push_back(j);
}

void SparseMatrix::ConvertToCSR(){
    /* This function converts the matrix from
    a COO to a CSR representation.
    */

    COO2CSR(this->a, this->i_idx, this->j_idx);
}

std::vector<double> SparseMatrix::MulVec(const std::vector<double> &vec){
    /* This function calculates the matrix-vector product between
    the matrix and the specified vector.
    
    Args:
        - std::vector<double> &vec: Vector to be multiplied.
        
    Returns:
        - std::vector<double> res: Result.
    */ 

    // initialize result vector
    int n = (int) vec.size();
    std::vector<double> res(n, 0.);

    // perform sparse multiplication
    for (int i = 0; i < (int) this->i_idx.size()-1; i++){
        for(int j = this->i_idx[i]; j < this->i_idx[i+1]; j++){
            res[i] += this->a[j] * vec[this->j_idx[j]];
        }
    }
    return res;
}
