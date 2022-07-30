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

### Converting n-ary contraints to binary constraints
### Unary Constraints
### Backtracking search
### Maintaining arc consistency during backtracking search
