import fileinput
import math

# Read input formula from stdin and return it as a string.
def getInputFormula():
	string = ""
	for line in fileinput.input():
		string += line
	return string

def getRoot(tree):
	clausesNoElements = []
	formula = getInputFormula()
	clauseList = formula.split("^")
	for i in range(0, len(clauseList)):
		clauseList[i] = clauseList[i].replace('(', '')
		clauseList[i] = clauseList[i].replace(')', '')
		clauseList[i] = clauseList[i].replace('\n', '')
		clauseList[i] = clauseList[i].split("V")
		clausesNoElements.append(len(clauseList[i]))
	literalsNo = max(clausesNoElements)
	tree.append(clauseList)
	maxNoNodes = pow(2, literalsNo + 1) - 1
	for i in range (1, maxNoNodes):
		tree.append(None)
	return tree, literalsNo, maxNoNodes

def addTree(tree, i, maxLevel, currentLevel):
	currentLiteral = str(currentLevel)
	currentFormula = tree[math.floor(i / 2)]
	if currentFormula == 1: 
		return 1
	if currentLevel < maxLevel:
		currentLiteral = str(currentLevel)
		currentFormula = tree[math.floor(i / 2)] # formula care trebuie prel.
		if i % 2 != 0:
			for clause in currentFormula:
				for literal in clause:
					if len(literal) > 1:
						aux = list(literal)
						if aux[0] == "~":
							if literal[1:] == currentLiteral:
								currentFormula.remove(clause)
								break
						if literal == currentLiteral:
							clause.remove(literal)
							if clause == []:
								currentFormula.remove(clause)
							break
					if literal == currentLiteral:
						clause.remove(literal)
						if clause == []:
							currentFormula.remove(clause)
						break
		else:
			for clause in currentFormula:
				for literal in clause:
					if literal == currentLiteral:
						currentFormula.remove(clause)
						break
					if len(literal) > 1:
						aux = list(literal)
						if aux[0] != "~":
							if literal[1:] == currentLiteral:
								currentFormula.remove(clause)
								break
						else:
							if literal[1:] == currentLiteral:
								clause.remove(literal)
								if clause == []:
									currentFormula.remove(clause)
								break
		if currentFormula == []:
			tree[i] = 1
		else:
			if currentLevel == maxLevel:
				tree[i] = 0
			else:
				tree[i] = currentFormula

		flag = addTree(tree, 2*i + 1, maxLevel, currentLevel + 1)
		if flag == 1:
			return 1
		return addTree(tree, 2*i, maxLevel, currentLevel + 1)
	else:
		return 0

	

def main():
	tree = []
	tree, literalsNo, maxNoNodes = getRoot(tree)
	print(addTree(tree, 1, literalsNo + 1, 1))

if __name__ == '__main__':
	main()
