import unicodedata
import sequitur as seq


# An encoded grammar stream is the right-hand side of every rule in 'G',
# separated by special character '#'
def encodeGrammar(G):
	grammarStream = ""
	for rule in range(0, len(G)):
		grammarStream += G[rule]
		if rule < len(G)-1:
			grammarStream += '#'
	return grammarStream


def compressionPerformance(input, stream, grammarStream):
	uncompressed = len(input)
	compressed = len(stream) + len(grammarStream)
	performance = uncompressed/compressed
	print('Compressed ' + str(uncompressed) + ' characters into ' + str(compressed))
	print('Performance score of ' + str(performance))


def main():
	print('Which text would you like to compress?')
	print('small input (enter 1)')
	print('DNA sequence (enter 2)')
	print('Shakespeare passage (enter 3)')
	fileName = input('enter text choice: ')
	if fileName == '1':
		fileName = 'smallinput.txt'
	elif fileName == '2':
		fileName = 'dna.txt'
	elif fileName == '3':
		fileName = 'shakespeare.txt'
	verbose = (input('Verbose mode? (y or n): ')).lower()
	if verbose == 'y':
		verbose = True
	elif verbose == 'n':
		verbose = False

	inputFile = open(fileName, 'r')
	inputText = inputFile.read()
	inputFile.close()
	print("Input text: " + inputText + '\n')

	# Sequitur
	G = seq.sequiturGrammar()
	seqStream, seqGrammar = G.sequitur(inputText, verbose)
	seqGrammarStream = encodeGrammar(seqGrammar)
	print('Symbol Stream:\n' + seqStream)
	print('Grammar Stream:\n' + seqGrammarStream + '\n')
	compressionPerformance(inputText, seqStream, seqGrammarStream)



main()