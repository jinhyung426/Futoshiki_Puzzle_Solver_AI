# Futoshiki Puzzle Solver - AI Program

CSC384H1S Artificial Intelligence - Assignment 2

This program implements a solver for Futoshiki Puzzle by formulating the game into 'Constraint Satisfaction Problem (CSP)'.


# propagators.py 
In <propagators.py> file, 3 Propagation methods are implemented.
1) Plain Backtracking (prop_BT)
2) Forward Checking (prop_FC)
3) GAC Propagation (prop_GAC)

Results show that GAC Propagation method and Forward Checking method solves the puzzle within significantly faster time
than when using plain backtracking, by pruning more states.


# futoshiki_csp.py
In <futoshiki_csp.py> file,
2 functions; futoshiki_csp_model_1 and futoshiki_csp_model_2 are implemented which builds a model of futoshiki grid. 

1) futoshiki_csp_model_1 : A model of a Futoshiki grid is built by using only binary not-equal constraints for both the row and column constraints.

2) futoshiki_csp_model_2 : A model of a Futoshiki grid built using only n-ary all-different constraints for both the row and column constraints


# model_mrv_test.py
<model_mrv_test.py> file contains test cases representing the initial board and constraints.
The program uses the model built in futoshiki_csp.py and propagators in propagators.py and computes the solution for the puzzle.
By comparing the result with its answer, the program outputs if the algorithm found the solution correctly and tells
how fast the algorithm computed the answer in terms of time and number of states that were checked.

As mentioned above, results show that GAC Propagation method and Forward Checking method solves the puzzle within significantly faster time than when using plain backtracking, by pruning more states. Also, model_1 computes the answer much faster than model_2.
