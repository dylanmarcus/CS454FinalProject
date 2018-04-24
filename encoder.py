import unicodedata
import itertools

# https://docs.python.org/3/library/itertools.html#itertools-recipes
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

#http://ls.pwd.io/2014/08/singly-and-doubly-linked-lists-in-python/
class Node(object):
 
    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next
 
 
class DoubleList(object):
 
    head = None
    tail = None
 
    def append(self, data):
        new_node = Node(data, None, None)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            new_node.next = None
            self.tail.next = new_node
            self.tail = new_node
 
    def remove(self, node_value):
        current_node = self.head
 
        while current_node is not None:
            if current_node.data == node_value:
                # if it's not the first element
                if current_node.prev is not None:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                else:
                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
                    self.head = current_node.next
                    current_node.next.prev = None
 
            current_node = current_node.next
 
    def show(self):
        print("Show list data:")
        current_node = self.head
        while current_node is not None:
            print(current_node.data)
            current_node = current_node.next
        print( "*"*50 )
 

class rule():
    def __init__(self, diagram, symbol):
        self.count = 1
        self.diagram = diagram
        self.phrase = symbol 

class encoder():

    def __init__(self, filename):
        self.diagrams = {}
        self.rules = []
        self.Uni = 191
        self.rulePos = 0
        with open(filename) as f:
           self.startRule = f.read()

    def nextUni(self):
        currentUni = chr(self.Uni)
        self.Uni += 1
        return currentUni

    def generateDiagramFreq(self):
        for (a,b) in pairwise(self.startRule):
            print('gendfreq',a,b)
            diagram = a + b
            #if the diagram exists add one to the rule count
            if diagram in self.diagrams:
                self.rules[ self.diagrams[diagram] ].count += 1
            #else add the diagram index to diagrams and append a new rule                       
            else:
                self.diagrams[ diagram ] = self.rulePos
                self.rulePos += 1
                self.rules.append( rule( diagram, self.nextUni() ) )

    def updateRuleCount(self, diagram ):
        self.rules[ self.diagrams[ diagram ] ]

    def replaceMostFreq(self):
        self.generateDiagramFreq()
        maxRule = max( self.rules, default=("",""), key=lambda r: r.count )
        if maxRule.count > 1:
            self.startRule = self.startRule.replace( maxRule.diagram, maxRule.phrase )
        #TODO else delete rule? track rules with count eq. 1 seperately?
        print(maxRule.phrase, maxRule.diagram, maxRule.count, \
              'Updated Start Rule==>', self.startRule )
        #TODO update rules count 
        return maxRule

    def compress(self):
        print('Before Most Frequent Update:', self.startRule)
        maxRule = self.replaceMostFreq()
        self.updateRuleCount( maxRule.count, maxRule.diagram )
        while maxRule.count > 1 and len(self.startRule) > 2:
            print('Before Most Frequent Update:', self.startRule)            
            maxRule = self.replaceMostFreq()
            self.updateRuleCount(maxRule.count, maxRule.diagram)                
        
        

def main():
    c = encoder('test.txt')
    d = DoubleList()
    d.append(1)
    d.append(5)
    d.append(10)
    d.append(15)
    d.show()
if __name__ == "__main__":
    main()
    
