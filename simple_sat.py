import fileinput

# Read input formula from stdin and return it as a string.
def getInputFormula():
	string = ""
	for line in fileinput.input():
		string += line
	return string

# Starting from the input formula, generate a matrix representation of it.
# First of all, get the number of clauses in formula (by spliting it at "^").
# Consider that number of clauses = number of lines in matrix.
# For each clause, get the number of literals (by spliting it at "V") and
# add it to a list.
# Consider that max value from this list = number of columns in matrix.
# Initialize a matrix (with dimensions calculated above) with zeros.
# To populate the matrix line by line check every literal from every clause:
# If it begins with "~", put "-1" in matrix in the corresponding position, else
# put "1" in matrix in the corresponding position.
# Return the matrix.
def getMatrix():
	clausesNoElements = []
	lineNo = 0
	formula = getInputFormula()					# get input
	clauseList = formula.split("^")				# split into clauses
	clauseNo = len(clauseList)					# get number of clauses
	for clause in clauseList:
		clause = clause.replace('(', '')
		clause = clause.replace(')', '')
		clause = clause.split("V")
		clausesNoElements.append(len(clause))
	literalsNo = max(clausesNoElements)			
	matrix = [[0 for i in range(literalsNo)] for j in range(clauseNo)]
	for clause in clauseList:
		clause = clause.replace('(', '')
		clause = clause.replace(')', '')
		clause = clause.split("V")
		for literal in clause:
			if len(literal) > 1:			 	# if literal has more than 1 char
				aux = list(literal)
				if aux[0] == "~":				# it's negated
					matrix[lineNo][int(literal[1:])-1] = -1
				else:
					matrix[lineNo][int(literal)-1] = 1
			else:								# it's pure
				matrix[lineNo][int(literal)-1] = 1
		lineNo += 1								# keep track of matrix line number
	return matrix

# Generate a binary representation (as a list) of a decimal @n on @listLen bites.
# This method is used to generate attributable values for the literals.
# It converts a decimal to binary and add zeros until the list has the required
# length.
def decimalToBinaryList(n, listLen):  
    binaryList = list(bin(n).replace("0b", ""))
    for i in range(0, len(binaryList)):
    	binaryList[i] = int(binaryList[i])
    for i in range (len(binaryList), listLen):
    	binaryList.insert(0, 0)
    return binaryList

# Get the largest number that can be represented on @bitesNo bites.
# This method is used to generate attributable values for the literals.
# Return the number.
def getLargestNo(bitesNo):
	l = [1 for i in range(0, bitesNo)]
	nr, k = 0, 1
	for i in range(0, len(l)):
		nr += k
		k <<= 1
	return nr

# Given a list of clauses as a matrix representation, determine if there exists
# an assignment that satisfies all of them simultaneously.
# For numbers starting from 0 to the largest number that can be represented on
# (@literalsNo bites + 1) get the binary representation. This representation 
# means a possible set of assignments.
# Check all existing literals line by line.
# If the literal exists (coresponding position in matrix is 1 or -1) and it's 
# assignment is 1 respectively 0, the line (clause) is evaluated as True. Else
# the line is evaluated as False.
# If one line is evaluated as False, the formula for current assignment set is
# evaluated as False -> move to the next set of assignments.s
def SAT(matrix):
	literalsNo = len(matrix[0])
	for i in range(0, getLargestNo(literalsNo) + 1):
		assignments = decimalToBinaryList(i, literalsNo)
		evaluateAssignment = 1					# initial state for formula
		for line in matrix:
			evaluateLine = 0					# initial state for clause
			for j in range(0, len(line)):
				if line[j] == 1:				# literal exists
					if assignments[j] == 1:		# it's assigned as True
						evaluateLine = 1		# enough to know that clause 
						break					# it's True
				if line[j] == -1:				# literal exists (negated)
					if assignments[j] == 0:		# it's assigned as False
						evaluateLine = 1		# enough to know that clause
						break					# it's Ture
			if evaluateLine == 0:				# clause it's Flase
				evaluateAssignment = 0			# enough to know that formula
				break							# it's False (it's not satisfiable)
		if evaluateAssignment == 1:				# formula it's true
			return 1							# it is satisfiable -> stop
	return 0									# no satifiable assigment set

def main():
	matrix = getMatrix()
	print(SAT(matrix))
	
if __name__ == '__main__':
	main()