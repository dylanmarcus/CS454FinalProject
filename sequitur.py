import unicodedata

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


class Grammar:

	def __init__(self):
		self.RULES = TwoWayDict()
		self.STARTRULE = ""
		self.PARENT = {}
		self.UNI = 191

#------------------------------------------------------------------------------

	def sequitur(self, input, verbose):
		diagramTable = []
		inputHead = 0
		while inputHead < len(input)-1:
			diagram = input[inputHead] + input[inputHead+1]
			if diagram not in diagramTable:
				diagramTable.append(diagram)
				if diagram in self.RULES:
					existingRule = self.RULES[diagram]
					self.STARTRULE += existingRule
					inputHead += 1
				else:
					self.STARTRULE += input[inputHead]
					if self.isSymbol(input[inputHead]):
						self.setParent(input[inputHead], '$')
			else:
				newRule = self.makeNewRule(diagram, '$')
				self.STARTRULE += newRule
				self.STARTRULE = self.applyRule(newRule, self.STARTRULE)
				inputHead += 1
				if self.isSymbol(diagram[0]):
					self.setParent(diagram[0], newRule)
				if self.isSymbol(diagram[1]):
					self.setParent(diagram[1], newRule)
				diagramTable = self.updateDiagramTable(diagramTable, self.STARTRULE)
			diagramTable = self.updateStartRule(self.STARTRULE, diagramTable)
			inputHead += 1

			if verbose:
				print("diagram: " + diagram)
				print("Diagram Table: " + str(diagramTable))
				self.printGrammarData()

		if inputHead == len(input)-1:
			self.STARTRULE += input[inputHead]
			self.updateStartRule(self.STARTRULE, diagramTable)
			self.validateRuleUtility()
			self.updateStartRule(self.STARTRULE, diagramTable)

		if verbose:
			self.printGrammarData()

		return self.STARTRULE, list(self.RULES.values())[::2]

#------------------------------------------------------------------------------

	def updateStartRule(self, input, diagramTable):
		newStartRule = ""
		newDiagramTable = []
		inputHead = 0
		while inputHead < len(input)-1:
			diagram = input[inputHead] + input[inputHead+1]
			if diagram not in newDiagramTable:
				newDiagramTable.append(diagram)
				if diagram in self.RULES:
					existingRule = self.RULES[diagram]
					newStartRule += existingRule
					inputHead += 1
				else:
					inputChar = input[inputHead]
					newDiagramTable.append(diagram)
					newStartRule += inputChar
					if self.isSymbol(inputChar):
						self.setParent(inputChar, '$')
			else:
				newRule = self.makeNewRule(diagram, '$')
				newStartRule += newRule
				newStartRule = self.applyRule(newRule, newStartRule)
				inputHead += 1
				if self.isSymbol(diagram[0]):
					self.setParent(diagram[0], newRule)
				if self.isSymbol(diagram[1]):
					self.setParent(diagram[1], newRule)
				newDiagramTable = self.updateDiagramTable(newDiagramTable, newStartRule)
			inputHead += 1
		if inputHead < len(input):
			newStartRule += input[inputHead]
		if newStartRule != self.STARTRULE:
			self.STARTRULE = newStartRule
			return newDiagramTable
		return diagramTable

#------------------------------------------------------------------------------

	def makeNewRule(self, diagram, parentRule):
		symbol = chr(self.UNI)
		self.UNI += 1
		self.RULES[symbol] = diagram
		self.setParent(symbol, parentRule)
		return symbol

#------------------------------------------------------------------------------

	def setParent(self, childRule, parentRule):
		if childRule in self.PARENT:
			if parentRule not in self.PARENT[childRule]:
				self.PARENT[childRule] += parentRule
		else:
			self.PARENT[childRule] = parentRule

#------------------------------------------------------------------------------

	def applyRule(self, rule, parentRule):
		parentRule = parentRule.replace(self.RULES[rule], rule)
		return parentRule

#------------------------------------------------------------------------------

	def updateDiagramTable(self, diagramTable, startRule):
		diagramTable = []
		for i in range(len(startRule)-1):
			diagramTable.append(startRule[i] + startRule[i+1])
		return diagramTable

#------------------------------------------------------------------------------

	def count(self, rule, parentRule):
		count = 0
		for char in parentRule:
			if char == rule:
				count += 1
		return count

#------------------------------------------------------------------------------

	def countChildRule(self, rule, parentRule, startRule):
		self.setParent(rule, parentRule)
		self.COUNTinStartRule[rule] = self.count(rule, '$')
		if rule in self.COUNTinOtherRules:
			self.COUNTinOtherRules[rule] += self.count(rule, self.RULES[parentRule])
		else:
			self.COUNTinOtherRules[rule] = self.count(rule, self.RULES[parentRule])

#------------------------------------------------------------------------------

	def isSymbol(self, x):
		if x in self.RULES:
			return True
		return False

#------------------------------------------------------------------------------

	def validateRuleUtility(self):
		rulesToDelete = []
		for rule in list(self.RULES.keys())[::2]:
			count = 0
			for parent in self.PARENT[rule]:
				if parent == '$':
					count += self.count(rule, self.STARTRULE)
				else:
					if parent in self.RULES:
						count += self.count(rule, self.RULES[parent])
			if count < 2:
				rulesToDelete.append(rule)
		for rule in rulesToDelete:
			self.deleteRule(rule)

#------------------------------------------------------------------------------

	def deleteRule(self, rule):
		for i in self.RULES[rule]:
			if self.isSymbol(i):
				for j in self.PARENT[rule]:
					self.setParent(i, j)
		for parent in self.PARENT[rule]:
			if parent == '$':
				self.STARTRULE = self.STARTRULE.replace(rule, self.RULES[rule])
			else:
				if parent in self.RULES:
					self.RULES[parent] = self.RULES[parent].replace(rule, self.RULES[rule])
		for parent in self.PARENT.values():
			parent = parent.replace(rule, '')
		del self.PARENT[rule]
		del self.RULES[rule]

#------------------------------------------------------------------------------

	def printGrammarData(self):
		print('Start Rule: ' + self.STARTRULE)
		print('Rules:')
		left = list(self.RULES.keys())[::2]
		right = list(self.RULES.values())[::2]
		for rule in range(len(left)):
			print(left[rule] + ' -> ' + right[rule])
		print('')

#------------------------------------------------------------------------------