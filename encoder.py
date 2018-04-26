import unicodedata
import itertools
import math

# https://docs.python.org/3/library/itertools.html#itertools-recipes
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

#http://ls.pwd.io/2014/08/singly-and-doubly-linked-lists-in-python/
class Node:

    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

    def hasChild(self):
        return (self.prev != None) or (self.next != None)

    def __repr__(self):
        return "<Node({})>".format(self.data)

class SequenceArray:

    head = None
    tail = None

    def __init__(self, capacity):
        self.pool = [ Node( None ) for _ in range(capacity) ]
        self.nextIndex = 0

    def newNode(self, data):
        tmpNode = self.pool[ self.nextIndex ]
        self.nextIndex += 1
        tmpNode.data = data
        return tmpNode

    #so max can be called on list instead of head
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next
        raise StopIteration

    def append(self, data):
        new_node = self.newNode(data)
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

    def __repr__(self):
        """
        current_node = self.head
        while current_node is not None:
            print(current_node.data)
            current_node = current_node.next
        print( "*"*50 )
        """
        #return "<SequenceArray(head={}, tail={})>".format(self.head, self.tail)
        return str(self.pool)

class DoubleList:

    head = None
    tail = None
    
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next
        raise StopIteration

    def append(self, node):
       
        if self.head is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            node.next = None
            self.tail.next = node
            self.tail = node

    def remove(self, node):
        if node.next is node.prev is None:
            return
        elif node is self.head:
            self.head = node.next
            self.head.prev = None
            node.prev = node.next = None
        elif node is self.tail:
            self.tail = node.prev
            self.tail.next = None
            node.prev = node.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            node.prev = node.next = None
        

    def show(self):
        print("Show list data:")
        current_node = self.head
        while current_node is not None:
            print(current_node.data)
            current_node = current_node.next
        print( "*"*50 )

    def __repr__(self):
        return str( list(self) )

class PriorityQueue:
    def __init__( self, size ):
        self.frequencyBins = [ DoubleList() for _ in range( size ) ]

    def updateFrequency(self, node):
        oldIndex = node.data.count - 3
        inLastBin = oldIndex >= len(self.frequencyBins) - 2
        inBin = oldIndex > 0
        #(count - 4) puts as at second to last bin the last bin stores different frequencies
        if inBin and not inLastBin:
            self.frequencyBins[ oldIndex ].remove(node)
        newIndex = oldIndex if inLastBin else oldIndex + 1
        self.frequencyBins[ newIndex ].append(node)

class PairRecord:
    def __init__(self, count, first):
        self.count = count
        self.first = first 

    def __repr__(self):
        return "<PairRecord({},{})>".format( self.count, self.first )


class Encoder:

    def __init__(self, filename):
        self.activePairs = {}
        self.Uni = 191
        with open(filename) as f:
            startRule = f.read()
        
        n = len(startRule)
        sizePq = math.ceil( math.sqrt(n) )
        #allocate exact space for sequence array
        self.sequenceArray = SequenceArray( n )
        #allocate space for priority queue 
        self.priorQueue = PriorityQueue( sizePq )
        for symbol in startRule:
            self.sequenceArray.append( symbol )

    def nextUni(self):
        currentUni = chr(self.Uni)
        self.Uni += 1
        return currentUni

    def generateDiagramFreq(self):
        for (a,b) in pairwise(self.sequenceArray):
            pair = a.data + b.data
            if pair not in self.activePairs:
                prNode = Node( PairRecord(1,a) )                
                self.activePairs[ pair ] = prNode 
            #pointers to pairs constant time
            prNode = self.activePairs[ pair ]
            if prNode.data.count == 1:
                prNode.data.count += 1
                self.priorQueue.updateFrequency( prNode )
            else:                
                prNode.data.count += 1
                self.priorQueue.updateFrequency( prNode )                                

    def updateRuleCount(self, rule ):
        self.priorQueue.append( rule )
        self.rules.remove( rule )
        self.diagrams = {}

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
        self.updateRuleCount( maxRule )
        while maxRule.count > 1 and len(self.startRule) > 2:
            print('Before Most Frequent Update:', self.startRule)
            maxRule = self.replaceMostFreq()
            self.updateRuleCount( maxRule )



def main():
    c = Encoder('test.txt')
    c.generateDiagramFreq()
    for bin in c.priorQueue.frequencyBins:
        bin.show()

if __name__ == "__main__":
    main()

