
import unicodedata


# used so a rule can be looked up by its left or right hand side
class TwoWayDict(dict):
    def __setitem__(self, key, value):
        # Remove any previous connections with these values
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)


def sequitur(input):
	STARTRULE = ""
	UNI = 191
	RULES = TwoWayDict()
	COUNT = {}
	PARENT = {}

	diagramTable = []
	diagram = ""

	inputHead = 0
	while inputHead < len(input)-1:
		diagram = input[inputHead] + input[inputHead+1]
		if diagram not in diagramTable:
			if diagram in RULES:
				STARTRULE += RULES[diagram]
				COUNT[RULES[diagram]] += 1
				inputHead += 1
			else:
				diagramTable.append(diagram)
				STARTRULE += input[inputHead]
		else:
			# add diagram to the start rule which will be soon replaced
			STARTRULE += diagram
			# create new rule
			RULES[chr(UNI)] = diagram
			COUNT[chr(UNI)] = 2
			UNI += 1
			# if an existing rule goes into this new rule, set its parent
			if diagram[0] in RULES or diagram[1] in RULES:
				setParent(diagram, RULES, PARENT)
			# apply new rule to the start rule
			STARTRULE = STARTRULE.replace(diagram, RULES[diagram])
			# update the diagram table
			diagramTable = []
			for i in range(len(STARTRULE)-1):
				diagramTable.append(STARTRULE[i] + STARTRULE[i+1])
			# make sure we don't read diagram[2] twice
			inputHead += 1
			
		diagramTable, STARTRULE, UNI = updateStartRule(diagramTable, STARTRULE, UNI, RULES, COUNT, PARENT)
		inputHead += 1

	if inputHead == len(input)-1:
		STARTRULE += input[inputHead]

	diagramTable, STARTRULE, UNI = updateStartRule(diagramTable, STARTRULE, UNI, RULES, COUNT, PARENT)
	return STARTRULE, RULES, COUNT


# This funciton is similar to sequirtur but is called to go through
# the starting rule to find new rules found by sequencing through 
# the starting rule as we would on an input string.
def updateStartRule(diagramTable, STARTRULE, UNI, RULES, COUNT, PARENT):
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
			# make new rule
			newStartRule += diagram
			RULES[chr(UNI)] = diagram
			COUNT[chr(UNI)] = 2
			UNI += 1
			# if an existing rule goes into this new rule, set its parent
			if diagram[0] in RULES or diagram[1] in RULES:
				setParent(diagram, RULES, PARENT)
			newStartRule = newStartRule.replace(diagram, RULES[diagram])
			newDiagramTable = []
			for i in range(len(newStartRule)-1):
				newDiagramTable.append(newStartRule[i] + newStartRule[i+1])
			# subtract 1 from the count of a rule that appears in this diagram
			if diagram[0] in RULES or diagram[1] in RULES:
				if diagram[0] in RULES:
					symbol = RULES[RULES[diagram[0]]]
					COUNT[symbol] -= 1
				if diagram[1] in RULES:
					symbol = RULES[RULES[diagram[1]]]
					COUNT[symbol] -= 1
				# does this rule not satisfy rule utility?
				if COUNT[symbol] < 2:
					# replace its symbol with its right-hand-side in its parent
					for p in PARENT[symbol]:
						RULES[p] = RULES[p].replace(symbol, RULES[symbol])
					# delete the unutilized rule
					del RULES[symbol]
					del COUNT[symbol]
					del PARENT[symbol]
			head += 1

		head += 1

	if head < len(STARTRULE):
		newStartRule += STARTRULE[head]
	if STARTRULE != newStartRule:
		return newDiagramTable, newStartRule, UNI

	return diagramTable, STARTRULE, UNI


def setParent(diagram, RULES, PARENT):
	if diagram[0] in RULES:
		if diagram[0] in PARENT:
			PARENT[diagram[0]] += RULES[diagram]
		else:
			PARENT[diagram[0]] = RULES[diagram]
	if diagram[1] in RULES:
		if diagram[1] in PARENT:
			PARENT[diagram[1]] += RULES[diagram]
		else:
			PARENT[diagram[1]] = RULES[diagram]



start, rules, count = sequitur("abcdbcabcd")
print(start)
print(rules)
print(count)