#ifndef MATVECOPS_HPP
#define MATVECOPS_HPP

#include <cmath>
#include <vector>

#include "sparse.hpp"

/* Collection of functions that handle matrix and vector operations needed for
the CG algorithm. */

std::vector<double> csr_matrix_vector_muliplication(const std::vector<double> &val, 
    const std::vector<int> &row_ptr, const std::vector<int> &col_idx,
    const std::vector<double> &b);

std::vector<double> vector_addition(const std::vector<double> &v1,
    const std::vector<double> &v2);

std::vector<double> vector_subtraction(const std::vector<double> &v1,
const std::vector<double> &v2);

std::vector<double> scalar_multiplication(double a, const std::vector<double> &v);

double l2_norm(const std::vector<double> &v);

double scalar_product(const std::vector<double> &v1,
const std::vector<double> &v2);

#endif
