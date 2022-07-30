# Kakuro-Solver
## Usage
### Input Format
The input is a text file.
First line contains the number of rows if the puzzle contains x rows then\
rows=x\
should be the first line, second line should be number of columns, if the puzzle contains y columns then \
columns=y \
should be the second line.\
The next line is\
Horizontal\
and after that the puzzle grid. \
All the cells should be seperated with commas, the empty cells should be 0, the grey cells should be a # character and the 
horizontal clues should have the number.\
Then there should be the line\
Vertical\
And after that the grid\
All the empty cells should be 0, the grey cells should be a # character and the 
vertical clues should have the number.\
\
Here is the example:\
\
![input0(2)](https://user-images.githubusercontent.com/75669598/181902924-43bebaef-53f2-4bca-9170-dadde2ff0c69.png)
\
rows=5\
columns=6\
Horizontal\
#,#,#,#,#,#\
4,0,0,#,#,#\
10,0,0,0,0,#\
#,10,0,0,0,0\
#,#,#,3,0,0\
Vertical\
#,3,6,#,#,#\
#,0,0,7,8,#\
#,0,0,0,0,3\
#,#,0,0,0,0\
#,#,#,#,0,0\
### Output format
If there is no solution the output file will have \
No solution\
else all the empty cells will be filled
## Working of the solver
### Kakuro puzzle as a CSP
The variables are the empty cells of the puzzle. As the cell can take values from domain of the variables is 1 to 9
The constraints are that the horizontal and vertical block of cells should be summing up to the number specified in the grey block such that all numbers in the block are distict.\
For Example:\
Let there be a continuous block of size n with corresponding S in which the continuous cells are x1,x2,x3,..xn.\
Constraints are:\
x1+x2+x3+...xn = S
and for i and j in 1 to n ,i!=j xi != xj and every cell has values from 1 to 9\
### Converting n-ary contraints to binary constraints
For every block with sum constraint S a new variable U is used which is a tuple and the sum of the numbers in tuple is S, the neighbours of U are the variables corresponding to the cell in that block.\
For example:\
Let x1, x2 form a block of cells with sum 3 and new variable U1 and x3, x4 form a block of cells with 4 and new variable U2.\
x1 + x2 = 3\
x3 + x4 = 6\
domain of x1 is [1,2,3,4,5,6,7,8,9]\
domain of x2 is [1,2,3,4,5,6,7,8,9]\
domain of x3 is [1,2,3,4,5,6,7,8,9]\
domain of x4 is [1,2,3,4,5,6,7,8,9]\
domain of U1 is [(1,2),(2,1)]\
domain of U2 is [(1,5),(2,4),(4,2),(5,1)]\
The domain can be further reduced of the variables as we know the smallest value in the cell is 1 so the value in a variable is 1 to min(9,S-1) where S is the sum of corresponding block.
### Backtracking search
The algorithm will substitute value for variables one by one and backtrack if conflict.
### Maintaining arc consistency during backtracking search
After assigning a value to a variable then the MAC algorithm is run to prune the domain.
