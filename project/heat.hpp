#ifndef HEAT_HPP
#define HEAT_HPP

#include <string>
#include <vector>

#include "CGSolver.hpp"
#include "sparse.hpp"


class HeatEquation2D
{
  private:
    SparseMatrix A;
    std::vector<double> b, x;
    double width;
    double height;
    double h;
    double tc;
    double th;
    int m;
    int n;

    /* Method to wrap x-indices around for periodic boudary */
    int PeriodicIndex(int i, int j);

    /* Method to get bottom boundary values at position x */
    double LowerBoundary(double x);

    /* Method to get top boundary values at position x */
    double UpperBoundary();

  public:
    /* Method to setup Ax=b system */
    int Setup(std::string inputfile);

    /* Method to solve system using CGsolver */
    int Solve(std::string soln_prefix);
};

#endif /* HEAT_HPP */
