

def sequitur(input):
	# starting rule is always at rules[0]
	rules = [""]
	diagramTable = []
	diagram = ""

	inputHead = 0
	while inputHead < len(input)-1:
		diagram = input[inputHead] + input[inputHead+1]
		if diagram not in diagramTable:
			if diagram in rules[1:]:
				rules[0] += str(rules.index(diagram))
				inputHead += 1
			else:
				diagramTable.append(diagram)
				try:
					rules[0] += input[inputHead]
				except TypeError:
					rules += input[inputHead]
		else:
			# add diagram to the start rule which will be soon replaced
			rules[0] += diagram
			# create new rule
			rules.append(diagram)
			# apply new rule to the start rule
			rules[0] = rules[0].replace(diagram, str(rules.index(diagram)))
			# update the diagram table
			diagramTable = []
			for i in range(len(rules[0])-1):
				diagramTable.append(rules[0][i] + rules[0][i+1])
			# make sure we don't read diagram[2] twice
			inputHead += 1
			
		if len(rules[0]) > 3:
			diagramTable = updateStartRule(rules, diagramTable)
		inputHead += 1

	if inputHead == len(input)-1:
		rules[0] += input[inputHead]

	diagramTable = updateStartRule(rules, diagramTable)
	return rules


# This funciton is similar to sequirtur but is called to go through
# the starting rule to find new rules found by sequencing through 
# the starting rule as we would on an input string.
def updateStartRule(rules, diagramTable):
	newStartRule = ""
	newDiagramTable = []
	diagram = ""

	head = 0
	while head < len(rules[0])-1:
		diagram = rules[0][head] + rules[0][head+1]
		if diagram not in newDiagramTable:
			newDiagramTable.append(diagram)
			newStartRule += rules[0][head]
		else:
			newStartRule += diagram
			rules.append(diagram)
			newStartRule = newStartRule.replace(diagram, str(rules.index(diagram)))
			newDiagramTable = []
			for i in range(len(newStartRule)-1):
				newDiagramTable.append(newStartRule[i] + newStartRule[i+1])
			head += 1

		head += 1

	if head < len(rules[0]):
		newStartRule += rules[0][head]
	if rules[0] != newStartRule:
		rules[0] = newStartRule
		return newDiagramTable

	return diagramTable



print(sequitur("abcdbcabcd"))