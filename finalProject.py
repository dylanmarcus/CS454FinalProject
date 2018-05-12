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


def main():
	inputFile = open('input.txt', 'r')
	inputText = inputFile.read()
	print("Input text:\n" + inputText)

	# Sequitur
	G = seq.Grammar()
	seqStream, seqGrammar = G.sequitur(inputText, True)
	seqGrammarStream = encodeGrammar(seqGrammar)
	print("Symbol Stream:\n" + seqStream)
	print("Grammar Stream:\n" + seqGrammarStream)


main()