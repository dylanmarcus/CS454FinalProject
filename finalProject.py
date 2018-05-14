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
	inputFile = open('shakespeare.txt', 'r')
	inputText = inputFile.read()
	inputFile.close()
	print("Input text: " + inputText + '\n')

	# Sequitur
	G = seq.Grammar()
	seqStream, seqGrammar = G.sequitur(inputText, False)
	seqGrammarStream = encodeGrammar(seqGrammar)
	print('Symbol Stream:\n' + seqStream)
	print('Grammar Stream:\n' + seqGrammarStream + '\n')
	compressionPerformance(inputText, seqStream, seqGrammarStream)



main()