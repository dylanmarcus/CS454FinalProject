import unicodedata

class rule():
    def __init__(self, diagram, symbol):
        self.count = 1
        self.right = diagram
        self.left = symbol 

class encoder():

    def __init__(self, filename):
        self.startRule = []
        self.diagrams = {}
        self.rules = []
        self.Uni = 191
        self.rulePos = 0
        with open(filename) as f:
            for line in f:
                for ch in line:
                    self.startRule.append(ch)
    #when rawdata is empty we need to know
    #so we return False
    def nextPair(self):
        if self.startRule == []:
            return []
        elif len(self.startRule) == 1:
            return self.startRule.pop(0)
        return self.startRule.pop(0) + self.startRule[0]

    def nextUni(self):
        currentUni = chr(self.Uni)
        self.Uni += 1
        return currentUni

    def inDiagramTable(self, d):
        if d in self.diagrams:
            return True
        return False

    def generateDiagramFreq(self):
        diagram = self.nextPair()
        if diagram == []:
            return
        #if the diagram exists add one to the rule count
        if diagram in self.diagrams:
            self.rules[ self.diagrams[diagram] ].count += 1
        #else add the diagram index to diagrams and append a new rule                       
        else:
            self.diagrams[ diagram ] = self.rulePos
            self.rulePos += 1
            self.rules.append( rule( diagram, self.nextUni() ) )
        self.generateDiagramFreq()
                
                                            
        
        

def main():
    c = encoder('test.txt')
    c.generateDiagramFreq()
    for rule in c.rules:
        print( rule.left + '-->' + rule.right + ';count: ' + str(rule.count) )
    



if __name__ == "__main__":
    main()
    
