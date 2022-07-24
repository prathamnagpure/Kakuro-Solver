from itertools import permutations

backtracking_count = 0
consistency_checks_by_backtracking = 0

#class to define the csp
class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domain = domain
        self.neighbours = neighbours
        self.constraints = constraints
        
#returns the number found in a line skipping other characters
def get_decimal_number(line):
    number = 0
    for z in line:
        if z.isdigit():
            number = number*10 + int(z)
    return number
    
#returns the domain values of a variable
def order_domain_values(csp, variable):
    return csp.domain[variable]
    
#if assigning the value to variable is consistent with previous assignments
#returns True
#else return False
def consistent(csp, variable, value, assignment):
    if variable[0] == "U":
        for neighbour in csp.neighbours[variable]:
            if neighbour in assignment:
                if assignment[neighbour] != value[csp.constraints[variable+neighbour]]:
                    return False
        return True
    else:
        for neighbour in csp.neighbours[variable]:
            if neighbour in assignment:
                if assignment[neighbour][csp.constraints[neighbour+variable]] != value:
                    return False
        return True

            
def remove_inconsistent_values(csp, xi, xj):
    removed = False
    for valueXi in csp.domain[xi]:
        remove = True
        for valueXj in csp.domain[xj]:
            if xj[0] == "U":
                if valueXi == valueXj[csp.constraints[xj+xi]]:
                    remove = False
                    break
            else:
                if valueXi[csp.constraints[xi+xj]] == valueXj:
                    remove = False
                    break
        if remove:
            csp.domain[xi].remove(valueXi)
            removed = True
    return removed

def AC_3(csp, queue=None):
    if queue == None:
        queue = [(xi,xj) for xi in csp.variables for xj in csp.neighbours[xi]]
    while queue:
        xi,xj = queue.pop(0)
        removed = remove_inconsistent_values(csp, xi, xj)
        if removed:
            if len(csp.domain[xi]) == 0:
                return False
            for neighbour in csp.neighbours[xi]:
                queue.append((neighbour, xi))
    return True
    
#finds a variable which is not assigned and returns it
def select_unassigned_variable(csp, assignment):
    for variable in csp.variables:
        if variable not in assignment:
            return variable

#recursive backtracking which returns solution or None
def recursive_backtracking(csp,assignment):
    global backtracking_count
    global consistency_checks_by_backtracking
    backtracking_count += 1
    if len(assignment) == len(csp.variables):
        return assignment
    variable = select_unassigned_variable(csp,assignment)
    for value in order_domain_values(csp, variable):
        consistency_checks_by_backtracking += 1
        if consistent(csp, variable, value, assignment):
            assignment[variable] = value
            result = recursive_backtracking(csp,assignment)
            if result != None:
                return result
    if variable in assignment:
        del assignment[variable]
    return None

def backtracking_search(csp):
    return recursive_backtracking(csp,{})
    
#Taking the input
file_name = input()
file_object = open(file_name, "r")
file_data = file_object.read().splitlines()
file_object.close()
get_decimal_number(file_data[0])
file_data = [i for i in file_data if i]
rows = get_decimal_number(file_data[0])
columns = get_decimal_number(file_data[1])
horizontal = [file_data[i].split(",") for i in range(3,3+rows)]
vertical = [file_data[i].split(",") for i in range(4+rows, 4+rows+rows)]
variables = []
domain = {}
constraints = {}
neighbours = {}
default_domain = [i for i in range(1,10)]
sum_constraint_found = False
sum_value = 0

#For the horizontal values
for i in range(rows):
    for j in range(columns):
        #Find sum clues
        if horizontal[i][j] != "#" and horizontal[i][j] != "0":
            u_variable_name = "UR"+str(i)+","+str(j)
            #Add the variable
            variables.append(u_variable_name)
            neighbours[u_variable_name] = []
            k = j + 1
            ct = 0
            #set the domains constraints neighbours variables of the block
            while k < columns:
                if horizontal[i][k] == "0":
                    x_variable_name = "X"+str(i)+","+str(k)
                    variables.append(x_variable_name)
                    neighbours[x_variable_name] = []
                    neighbours[x_variable_name].append(u_variable_name)
                    neighbours[u_variable_name].append(x_variable_name)
                    domain[x_variable_name] = [l for l in range(1,min(int(horizontal[i][j]),10))]
                    constraints[u_variable_name+x_variable_name] = ct
                    ct += 1
                else:
                    break
                k += 1
            domain[u_variable_name] = [lst for lst in permutations([1,2,3,4,5,6,7,8,9],k-j-1) if sum(lst) == int(horizontal[i][j])]
            j = k

#For the vertical values
for j in range(columns):
    for i in range(rows):
        #find the sum clues
        if vertical[i][j] != "#" and vertical[i][j] != "0":
            u_variable_name = "UD"+str(i)+","+str(j)
            #Add the variable
            variables.append(u_variable_name)
            neighbours[u_variable_name] = []
            k = i + 1
            ct = 0
            #set the domains constraints neighbours variables in block
            while k < rows:
                if vertical[k][j] == "0":
                    x_variable_name = "X"+str(k)+","+str(j)
                    if x_variable_name not in variables:
                        variables.append(x_variable_name)
                    if x_variable_name in neighbours:
                        neighbours[x_variable_name].append(u_variable_name)
                    else:
                        neighbours[x_variable_name] = [u_variable_name]
                    neighbours[u_variable_name].append(x_variable_name)
                    if x_variable_name in domain:
                        domain[x_variable_name] = list(set(domain[x_variable_name]).intersection(set([l for l in range(1,min(int(vertical[i][j]),10))])))
                    else:
                        domain[x_variable_name] = [l for l in range(1,min(int(vertical[i][j]),10))]
                    constraints[u_variable_name+x_variable_name] = ct
                    ct += 1
                else:
                    break
                k += 1
            domain[u_variable_name] = [lst for lst in permutations([1,2,3,4,5,6,7,8,9],k-i-1) if sum(lst) == int(vertical[i][j])]
            i = k
#set the csp
csp = CSP(variables, domain, neighbours, constraints)
#apply arc consistency on all arcs
AC_3(csp)
#Find the solution by backtracking search
assignment = backtracking_search(csp)

print("backtracking calls",backtracking_count)
print("consistency checks by backtracking",consistency_checks_by_backtracking)

#To get the outputfile named with the number of input file
output_file_name = "output" + str(get_decimal_number(file_name)) + ".txt"
out_file_object = open(output_file_name, 'w+')
out_file_object.write(file_data[0] + "\n")
out_file_object.write(file_data[1] + "\n")
out_file_object.write(file_data[2] + "\n")
for i in range(rows):
    for j in range(columns):
        if horizontal[i][j] == '#' or horizontal[i][j] != '0':
            out_file_object.write(horizontal[i][j])
        else:
            out_file_object.write(str(assignment["X"+str(i)+","+str(j)]))
        if j != columns - 1:
                out_file_object.write(",")
    out_file_object.write("\n")
out_file_object.write(file_data[3+rows] + "\n")
for i in range(rows):
    for j in range(columns):
        if horizontal[i][j] == '#' or horizontal[i][j] != '0':
            out_file_object.write(vertical[i][j])
        else:
            out_file_object.write(str(assignment["X"+str(i)+","+str(j)]))
        if j != columns - 1:
                out_file_object.write(",")
    out_file_object.write("\n")
            







            
