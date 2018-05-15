import unicodedata
import itertools
import math

SYMBOL = 0 
INDEX = 1

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
    
    def __iter__(self):
        yield self
        node = self.next
        while node is not None and node is not self:
            yield node
            node = node.next
        raise StopIteration

    def hasChild(self):
        return (self.prev != None) or (self.next != None)

    def __repr__(self):
        return "<Node({})>".format(self.data)

class SequenceArray:

    def __init__(self, capacity):
        self.pool = [ Node( None ) for _ in range(capacity) ]
        self.nextIndex = 0

    def newNode(self, data):
        tmpNode = self.pool[ self.nextIndex ]
        tmpNode.data = (data, self.nextIndex) 
        self.nextIndex += 1
        return tmpNode

    #so max can be called on list instead of head
    def __iter__(self):
        return iter(self.pool)

    def append(self, data):
        new_node = self.newNode(data)
        new_node.prev = new_node
        new_node.next = new_node

    def remove(self, item ):
        nextIndex = item.data[INDEX] + 1
        item.data = None
        if nextIndex < self.nextIndex:
            nextItem = self.pool[nextIndex]
            if nextItem.data is None:
                item.next = nextItem.next
            else:
                item.next = nextItem
        else:
            item.next = None

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
#Test Remove
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
            node.prev = node.next = None
        else:
            node.prev = self.tail
            node.next = None
            self.tail.next = node
            self.tail = node

    def remove(self, node):
        assert self.head is not None, self.tail is not None
        if node is self.head:
            if node is self.tail:
                self.head = self.tail = None
            else:
                self.head = self.head.next
                self.head.prev = None
        elif node is self.tail:
            self.tail.prev.next = None
            self.tail = self.tail.prev
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
        inBin = oldIndex >= 0
        #(count - 4) puts as at second to last bin the last bin stores different frequencies
        if inBin and not inLastBin:
            print(self.frequencyBins[oldIndex].head,'in update')
            self.frequencyBins[ oldIndex ].remove(node)
        newIndex = (len(self.frequencyBins) - 1) if inLastBin else oldIndex + 1
        self.frequencyBins[ newIndex ].append(node)

class PairRecord:
    def __init__(self, count, first):
        self.count = count
        self.first = first 

    def __repr__(self):
        return "<PairRecord(count: {}, first: {})>".format( self.count, self.first )

def linkPair(first, last):
    oldPrev = first.prev
    oldPrev.next = last
    first.prev = last
    last.prev = oldPrev
    last.next = first

class Encoder:

    def __init__(self, input):
        self.activePairs = {}
        with open(input) as f:
            startRule = f.read()
        n = len(startRule)
        self.uniInt = 191
        self.sizePq = math.ceil( math.sqrt(n) )
        #allocate exact space for sequence array
        self.sequenceArray = SequenceArray( n )
        #allocate space for priority queue 
        self.priorQueue = PriorityQueue( self.sizePq )
        for symbol in startRule:
            self.sequenceArray.append( symbol )

    def generateDiagramFreq(self):
        #we don't want empty records
        for (a,b) in pairwise( node for node in self.sequenceArray if node.data is not None ):
            pair = a.data[SYMBOL] + b.data[SYMBOL]
            print('######',pair,'###########')
            if pair not in self.activePairs:
                prNode = Node( PairRecord(1,a) )                
                self.activePairs[ pair ] = prNode 
                continue
            prNode = self.activePairs[ pair ]
            prNode.data.count += 1
            linkPair( prNode.data.first , a )
            self.priorQueue.updateFrequency( prNode )                                

    def updateRuleCount(self, rule ):
        self.priorQueue.append( rule )
        self.rules.remove( rule )
        self.diagrams = {}

    def nextUni(self):
        uni = chr(self.uniInt)
        self.uniInt += 1
        return uni
        
    def replaceMostFreq(self):
        maxPr = None
        revBins = reversed( self.priorQueue.frequencyBins )
        lastBin = next(revBins)
        if lastBin.head is not None:
            maxPr = max( lastBin, key=lambda x: x.data.count )
        else:
            for bin in revBins:
                if bin.head is not None:
                    maxPr = bin.head
                    break
        if maxPr is None:
            return False
        #        self.priorQueue.remove( maxPr )
        UNI = self.nextUni()
        for this in maxPr.data.first:
            index = this.data[INDEX]
            newnode = Node( (UNI,index) )
            newnode.prev = newnode
            newnode.next = newnode
            self.sequenceArray.pool[index] = newnode
            nextnode = None
            nextnextnode = None
            #there is a next thing
            if (index + 1) < self.sequenceArray.nextIndex:
                nextnode = self.sequenceArray.pool[index + 1]
                nextnode.data = None
                if (index + 2) < self.sequenceArray.nextIndex:
                    nextnextnode = self.sequenceArray.pool[index + 2]
                    nextnode.next = nextnextnode
                    nextnode.prev = nextnode
                else:
                    nextnode.prev = nextnode
                    nextnode.next = None
        return True
    
def replaceMax( encoder, uINT ):
    maxPR = max( encoder.activePairs.values(), key=lambda x: x.data.count )
    PRcount = maxPR.data.count
    maxrulefirst = maxPR.data.first
    print('maxrule firsts')
    for x in maxrulefirst:
        print(x)
    UNI = chr(uINT)
    input = []
    if PRcount > 1:
        for ap in maxrulefirst:
            tmp = encoder.sequenceArray.pool[ ap[INDEX] ]
            newnode = Node( (UNI, ap[INDEX]) )
            print( tmp.data,'inmaxrul')
            encoder.sequenceArray.pool[ ap[INDEX] ] = newnode
            encoder.sequenceArray.pool.pop( ap[INDEX] + 1 )
        for x in encoder.sequenceArray:
            input.append(x.data[SYMBOL])
    return input

#final res -> (stream, grammer)
def main():
    star = "*"
    repair = Encoder('test.txt')
    repair.generateDiagramFreq()
    for x in repair.sequenceArray:
        print(x)
    while repair.replaceMostFreq():
        print(star*50)
        for x in repair.sequenceArray:
            print(x)

        repair.generateDiagramFreq()
        
    '''
    for x in repair.sequenceArray:
        print(x)
    print(star*50)
    repair.generateDiagramFreq()
    for x in repair.sequenceArray:
        print(x)
    repair.replaceMostFreq()
    for x in repair.sequenceArray:
        print(x)
    '''
    '''
    repair.replaceMostFreq()
    print(star*50)
    for x in repair.sequenceArray:
        print(x)
    print(star*50)
    repair.generateDiagramFreq()
    repair.replaceMostFreq()
    for x in repair.sequenceArray:
        print(x)
    '''
    '''    
    print('after replacement')
    for x in repair.sequenceArray:
        print(x)
    repair.generateDiagramFreq()
    print('after second gen dia freq')
    repair.replaceMostFreq()
    print('after replacement')
    for x in repair.sequenceArray:
        print(x)
    '''
    '''
    uniInt = 191
    startRule = ""
    print('start rule')
    for x in c.sequenceArray:
        startRule += x.data[SYMBOL]
    print(startRule)
    c.generateDiagramFreq()
    input = replaceMax( c, uniInt )
    print(':',input)
    uniInt += 1
    while input != []:
        c = Encoder( input, False)
        c.generateDiagramFreq()
        input = replaceMax(c,uniInt)
        uniInt += 1
        print(input)
    startRule = ""
    print('start rule')
    for x in c.sequenceArray:
        startRule += x.data[SYMBOL]
    print(startRule)

    '''
    '''
    print('uniInt',uniInt)
    print('len input', len(input) )
    for x in input:
        print(x)
        
    d = Encoder(input,False)
    d.generateDiagramFreq()
    input = replaceMax( d, uniInt )
    uniInt += 1
    print('uniInt',uniInt)
    print('len input', len(input) )
    for x in input:
        print(x)
    d = Encoder(input,False)
    d.generateDiagramFreq()
    input = replaceMax( d,uniInt )
    uniInt += 1
    print('uniInt',uniInt)
    print('len input', len(input) )
    for x in input:
        print(x)
    '''
    '''       
    print("after second pass")
    for x in input:
        print(x)
    c = Encoder( input, False )
    c.generateDiagramFreq()
    input = replaceMax( c, uniInt )
    
    print("after third pass")
    for x in input:
        print(x)
    '''
    '''
    newindex = 0
    for x in c.sequenceArray:
        sym, idx = x.data
        x.data = (sym, newindex)
        newindex += 1
    for x in c.sequenceArray:
        print(x)

    c.activePairs = {}
    c.priorQueue = PriorityQueue( c.sizePq )
    c.generateDiagramFreq()
    print('after second pass' )
    maxrulefirst = max( c.activePairs.values(), key=lambda x: x.data.count ).data.first

    for x in c.priorQueue.frequencyBins:
        print( x )
    '''
    '''
    for n in c.sequenceArray:
        print( n )
    c.activePairs = {}
    c.generateDiagramFreq()
    for ap in c.sequenceArray:
        print( ap )
    ''' 
    '''
    for bin in reversed(c.priorQueue.frequencyBins):
        bin.show()
    pr = next(iter(c.priorQueue.frequencyBins[3]))
    first = pr.data.first 
    for f in first:
        print(f)
    ''' 
if __name__ == "__main__":
    main()

