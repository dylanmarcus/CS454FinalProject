
import unicodedata


def sequitur(input):
	STARTRULE = ""
	UNI = 191
	RULES = {}

	diagramTable = []
	diagram = ""

	inputHead = 0
	while inputHead < len(input)-1:
		diagram = input[inputHead] + input[inputHead+1]
		if diagram not in diagramTable:
			if diagram in RULES:
				STARTRULE += RULES[diagram][0]
				RULES[diagram][1] += 1
				print(RULES[diagram][0] + " inc: " + str(RULES[diagram][1]))
				inputHead += 1
			else:
				diagramTable.append(diagram)
				STARTRULE += input[inputHead]
		else:
			# add diagram to the start rule which will be soon replaced
			STARTRULE += diagram
			# create new rule
			RULES.update({diagram: [chr(UNI), 2]})
			print(RULES[diagram][0] + " new: " + str(RULES[diagram][1]))
			UNI += 1
			# apply new rule to the start rule
			STARTRULE = STARTRULE.replace(diagram, RULES[diagram][0])
			# update the diagram table
			diagramTable = []
			for i in range(len(STARTRULE)-1):
				diagramTable.append(STARTRULE[i] + STARTRULE[i+1])
			# make sure we don't read diagram[2] twice
			inputHead += 1
			
		diagramTable, STARTRULE, UNI = updateStartRule(diagramTable, STARTRULE, UNI, RULES)
		inputHead += 1

	if inputHead == len(input)-1:
		STARTRULE += input[inputHead]

	diagramTable, STARTRULE, UNI = updateStartRule(diagramTable, STARTRULE, UNI, RULES)
	return STARTRULE, RULES


# This funciton is similar to sequirtur but is called to go through
# the starting rule to find new rules found by sequencing through 
# the starting rule as we would on an input string.
def updateStartRule(diagramTable, STARTRULE, UNI, RULES):
	newStartRule = ""
	newDiagramTable = []
	diagram = ""

	head = 0
	while head < len(STARTRULE)-1:
		diagram = STARTRULE[head] + STARTRULE[head+1]
		if diagram not in newDiagramTable:
			newDiagramTable.append(diagram)
			newStartRule += STARTRULE[head]
		else:
			newStartRule += diagram
			RULES.update({diagram: [chr(UNI), 2]})
			UNI += 1
			newStartRule = newStartRule.replace(diagram, RULES[diagram][0])
			newDiagramTable = []
			for i in range(len(newStartRule)-1):
				newDiagramTable.append(newStartRule[i] + newStartRule[i+1])
			head += 1

		head += 1

	if head < len(STARTRULE):
		newStartRule += STARTRULE[head]
	if STARTRULE != newStartRule:
		return newDiagramTable, newStartRule, UNI

	return diagramTable, STARTRULE, UNI



start, rules = sequitur("abcdbcabcd")
print(start)
print(rules)