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
    
    #added default init values for prev and next
    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next
        
    #added iter functionality to prefab class
    def __iter__(self):
        yield self
        node = self.next
        while node is not None and node is not self and node.next is not node:
            yield node
            node = node.next
        raise StopIteration

    def hasChild(self):
        return (self.prev != None) or (self.next != None)

    #added iter functionality to prefab class
    def __repr__(self):
        return "<Node({})>".format(self.data)

#this data strucutred stores nodes where the data is a pair
#containing with the first being a symbol and the second an index
#to the current position in the sequence array
#the nodes next and prev are set to self on init and will point to
#repeated occurences of the left most thing in repeated pairs
#THIS ALLOWS FOR REPLACEMENT OF MOST FREQUENT PAIRS IN CONSTANT TIME
class SequenceArray:

    def __init__(self, capacity):
        self.pool = [ Node( None ) for _ in range(capacity) ]
        self.nextIndex = 0

    def newNode(self, data):
        tmpNode = self.pool[ self.nextIndex ]
        tmpNode.next = tmpNode
        tmpNode.prev = tmpNode
        tmpNode.data = (data, self.nextIndex) 
        self.nextIndex += 1
        return tmpNode

    #so max can be called on list instead of head
    def __iter__(self):
        return iter(self.pool)

    def append(self, data):
        new_node = self.newNode(data)

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

    def getNext(self, node):
        if node.data is None:
            return node.next
        
        index = node.data[INDEX] + 1
        if index < len(self.pool):
            nextNode = self.pool[index]
            if nextNode.data is None:
                nextNode = nextNode.next
            else:
                assert nextNode.data is not None
        else:
            nextNode = None
        return nextNode

    def deleteNext(self, node ):
        oldNext = self.getNext(node)
        assert oldNext is not None
        newNext = self.getNext( oldNext )
        oldNext.next = newNext
        oldNext.prev = oldNext.data = None

    
    def __repr__(self):
        return str(self.pool)

#this data structure is used to link pairs of symbols with the
#same number of counts but different symbols values
#a node in the list points                                       
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
            current_node = current_node.next
        print( "*"*50 )

    def __repr__(self):
        return str( list(self) )

class PriorityQueue:
    def __init__( self, size ):
        self.frequencyBins = [ DoubleList() for _ in range( size ) ]
        self.maxIndex = size - 1
        
    def updateFrequency(self, node):
        oldIndex = node.data.count - 3
        inLastBin = oldIndex >= len(self.frequencyBins) - 2
        inBin = oldIndex >= 0
        #(count - 4) puts as at second to last bin the last bin stores different frequencies
        if inBin and not inLastBin:
            self.frequencyBins[ oldIndex ].remove(node)
        newIndex = (len(self.frequencyBins) - 1) if inLastBin else oldIndex + 1
        self.frequencyBins[ newIndex ].append(node)

    def remove( self, node ):
        index = node.data.count - 2
        inLastBin = index >= self.maxIndex
        if not inLastBin:
            tmpList = self.frequencyBins[index]
            tmpList.remove( node )
        else:
            tmpList = self.frequencyBins[ self.maxIndex ]
            tmpList.remove( node )
            
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

    def __init__(self, input, isFile,uniInt):
        self.activePairs = {}
        if isFile:
            with open(input) as f:
                self.startRule = f.read()
        else:
            self.startRule = input
        self.uniInt = uniInt
        n = len(self.startRule)
        self.sizePq = math.ceil( math.sqrt(n) )
        #allocate exact space for sequence array
        self.sequenceArray = SequenceArray( n )
        #allocate space for priority queue 
        self.priorQueue = PriorityQueue( self.sizePq )
        for symbol in self.startRule:
            self.sequenceArray.append( symbol )

    def generateDiagramFreq(self):
        #we don't want empty records
        for (a,b) in pairwise( node for node in self.sequenceArray if node.data is not None ):
            pair = a.data[SYMBOL] + b.data[SYMBOL]
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
            return( "","","","")
        self.priorQueue.remove( maxPr )
        UNI = self.nextUni()
        for this in maxPr.data.first:
            if this.data is None:
                continue

            #index of replaced thing
            index = this.data[INDEX]
            #is the thing in the array None it has been removed
            if self.sequenceArray.pool[index].data is None:
                continue
            #create node to replace left thing
            newnode = Node( (UNI,index) )
            newnode.prev = newnode
            newnode.next = newnode
            #replace the old node
            lPart = this.data[SYMBOL]
            rthing = self.sequenceArray.pool[index + 1]
            rPart = rthing.data[SYMBOL]
            self.sequenceArray.pool[index] = newnode
            self.sequenceArray.deleteNext(newnode)

        return( "".join(n.data[SYMBOL] for n in self.sequenceArray if n.data is not None),lPart,rPart,UNI)
    
def replaceMax( encoder, uINT ):
    maxPR = max( encoder.activePairs.values(), key=lambda x: x.data.count )
    PRcount = maxPR.data.count
    maxrulefirst = maxPR.data.first
    UNI = chr(uINT)
    input = []
    if PRcount > 1:
        for ap in maxrulefirst:
            tmp = encoder.sequenceArray.pool[ ap[INDEX] ]
            newnode = Node( (UNI, ap[INDEX]) )
            encoder.sequenceArray.pool[ ap[INDEX] ] = newnode
            encoder.sequenceArray.pool.pop( ap[INDEX] + 1 )
        for x in encoder.sequenceArray:
            input.append(x.data[SYMBOL])
    return input

#final res -> (stream, grammer)
def main():
    star = "*"
    repair = Encoder('shakespeare.txt', True, 191)
    lenStart = len( repair.startRule )
    repair.generateDiagramFreq()
    input,l,r,u = repair.replaceMostFreq()
    rules = []
    while input != "":
        rules.append( (u,l+r) )
        lenEnd = len( input )
        repair = Encoder(input, False, repair.uniInt)
        repair.generateDiagramFreq()
        input,l,r,u = repair.replaceMostFreq()
    
    for x in rules:
        print(x[0] ,'->',x[1])

    print('compression ratio', lenStart/lenEnd , 'to 1' )


if __name__ == "__main__":
    main()

