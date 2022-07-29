from itertools import permutations
from copy import deepcopy

#backtracking_count = 0
#consistency_checks_by_backtracking = 0

#class to define the csp
class KakuroCSP:
    def __init__(self, variables, domain, neighbours, constraints):
        self.variables = variables
        self.domain = domain
        self.neighbours = neighbours
        self.constraints = constraints
        
    #returns the domain values of a variable
    def order_domain_values(self, variable):
        return self.domain[variable]
 
    #if assigning the value to variable is consistent with previous assignments
    #returns True
    #else return False
    def consistent(self, variable, value, assignment):
    #checking if the variable is a empty cell variable or the one assigned with constraints
        if variable[0] == "U":
            for neighbour in self.neighbours[variable]:
                if neighbour in assignment:
                    if assignment[neighbour] != value[self.constraints[variable+neighbour]]:
                        return False
            return True
        else:
            for neighbour in self.neighbours[variable]:
                if neighbour in assignment:
                    if assignment[neighbour][self.constraints[neighbour+variable]] != value:
                        return False
            return True

    #removes the inconsistent values from the domain and prunes the domain
    #returns true if a value is removed
    def remove_inconsistent_values(self, xi, xj):
        removed = False
        for valueXi in self.domain[xi]:
            remove = True
            for valueXj in self.domain[xj]:
                if xj[0] == "U":
                    if valueXi == valueXj[self.constraints[xj+xi]]:
                        remove = False
                        break
                else:
                    if valueXi[self.constraints[xi+xj]] == valueXj:
                        remove = False
                        break
            if remove:
                self.domain[xi].remove(valueXi)
                removed = True
        return removed
    #finds a variable which is not assigned and returns it
    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

#The AC-3 algorithm returns false if the domain becomes empty of some variable
def AC_3(csp, queue=None):
    if queue == None:
        queue = [(xi,xj) for xi in csp.variables for xj in csp.neighbours[xi]]
    while queue:
        xi,xj = queue.pop(0)
        removed = csp.remove_inconsistent_values(xi, xj)
        if removed:
            if len(csp.domain[xi]) == 0:
                return False
            #add the neighbour arcs in queue if some value is removed
            for neighbour in csp.neighbours[xi]:
                queue.append((neighbour, xi))
    return True
            
# Maintaining arc consistency by calling AC-3 with the queue with only arcs of
#neighbours of variable
def MAC(csp, variable, assignment):
    queue = [(neighbour,variable) for neighbour in csp.neighbours[variable] if neighbour not in assignment]
    return AC_3(csp, queue)

#recursive backtracking with mac which returns solution or None
def recursive_backtracking_with_MAC(csp,assignment):
    #global backtracking_count
    #global consistency_checks_by_backtracking
    #backtracking_count += 1
    #If all values assigned then return the assignment
    if len(assignment) == len(csp.variables):
        return assignment
    variable = csp.select_unassigned_variable(assignment)
    for value in csp.order_domain_values(variable):
        #consistency_checks_by_backtracking += 1
        if csp.consistent(variable, value, assignment):
            #assign a value to variable
            assignment[variable] = value
            #set the domain of variable as the assigned value
            csp.domain[variable] = [value]
            #save the domain
            saved_domain = deepcopy(csp.domain)
            #prune the domain and if no domain is empty
            if MAC(csp, variable, assignment):
                #recursively call backtracking
                result = recursive_backtracking_with_MAC(csp,assignment)
                if result != None:
                    return result
            #restore domain back 
            csp.domain = deepcopy(saved_domain)
    #restore the assignment
    if variable in assignment:
        del assignment[variable]
    return None

def backtracking_search_with_MAC(csp):
    return recursive_backtracking_with_MAC(csp,{})

#returns the number found in a line skipping other characters
def get_decimal_number(line):
    number = 0
    for z in line:
        if z.isdigit():
            number = number*10 + int(z)
    return number
    
def make_kakuro_csp(number_of_rows,number_of_columns,horizontal,vertical):
    variables = []
    domain = {}
    constraints = {}
    neighbours = {}
    
    #For the horizontal values
    for i in range(number_of_rows):
        for j in range(number_of_columns):
            #Find sum clues
            if horizontal[i][j] != "#" and horizontal[i][j] != "0":
                u_variable_name = "UR" + str(i) + "," + str(j)
                #Add the variable
                variables.append(u_variable_name)
                neighbours[u_variable_name] = []
                k = j + 1
                ct = 0
                #set the domain, constraints, neighbours and variables of the block
                while k < number_of_columns:
                    if horizontal[i][k] == "0":
                        x_variable_name = "X" + str(i) + "," + str(k)
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
    for j in range(number_of_columns):
        for i in range(number_of_rows):
            #find the sum clues
            if vertical[i][j] != "#" and vertical[i][j] != "0":
                u_variable_name = "UD"+str(i)+","+str(j)
                #Add the variable
                variables.append(u_variable_name)
                neighbours[u_variable_name] = []
                k = i + 1
                ct = 0
                #set the domains constraints neighbours variables in block
                while k < number_of_rows:
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
    #return the csp
    return KakuroCSP(variables, domain, neighbours, constraints)

#To get the outputfile named with the number of input file
def write_solution_to_output_file(output_file_name,input_file_data,horizontal,vertical,number_of_rows,number_of_columns,assignment):
    out_file_object = open(output_file_name, 'w+')
    out_file_object.write(input_file_data[0] + "\n")
    out_file_object.write(input_file_data[1] + "\n")
    out_file_object.write(input_file_data[2] + "\n")
    for i in range(number_of_rows):
        for j in range(number_of_columns):
            if horizontal[i][j] == '#' or horizontal[i][j] != '0':
                out_file_object.write(horizontal[i][j])
            else:
                out_file_object.write(str(assignment["X"+str(i)+","+str(j)]))
            if j != number_of_columns - 1:
                    out_file_object.write(",")
        out_file_object.write("\n")
    out_file_object.write(input_file_data[3+number_of_rows] + "\n")
    for i in range(number_of_rows):
        for j in range(number_of_columns):
            if horizontal[i][j] == '#' or horizontal[i][j] != '0':
                out_file_object.write(vertical[i][j])
            else:
                out_file_object.write(str(assignment["X"+str(i)+","+str(j)]))
            if j != number_of_columns - 1:
                    out_file_object.write(",")
        out_file_object.write("\n")
    out_file_object.close()
    
def main():
    input_file_name = input("Enter the path of the kakuro puzzle file: ")
    input_file_object = open(input_file_name, "r")
    output_file_name = input("Enter the path of the output file in which answer will be displayed: ")
    input_file_data = input_file_object.read().splitlines()
    input_file_object.close()
    
    number_of_rows = get_decimal_number(input_file_data[0])
    number_of_columns = get_decimal_number(input_file_data[1])
    horizontal = [input_file_data[i].split(",") for i in range(3,3+number_of_rows)]
    vertical = [input_file_data[i].split(",") for i in range(4+number_of_rows, 4+2*number_of_rows)]
    csp = make_kakuro_csp(number_of_rows,number_of_columns,horizontal,vertical)
    #apply arc consistency on all arcs
    AC_3(csp)
    #Find the solution by backtracking search
    assignment = backtracking_search_with_MAC(csp)
    #print("backtracking calls",backtracking_count)
    #print("consistency checks by backtracking",consistency_checks_by_backtracking)
    if assignment == None:
        print("No solution")
    else:
        write_solution_to_output_file(output_file_name,input_file_data,horizontal,vertical,number_of_rows,number_of_columns,assignment)
        
if __name__ == "__main__":
    main()


   
   
   
   
   
   
