#!/usr/bin/python
from collections import defaultdict
from math import log
import re
import nltk
import sys
import getopt

"""
Final static values
"""
NGRAM_SIZE = 4
MALAY = 'malaysian'
TAMIL = 'tamil'
INDONESIAN = 'indonesian'


"""
Helper functions used in build_LM
"""

def extract_Language(line):
    language = line.split()[0].lower()
    if (language != 'indonesian' and language != 'malaysian' and language != 'tamil'):
        print 'Language is not valid in input.train.txt'
        sys.exit(0)
    else:
        return language

def create_NPadding(sizeOfN):
    tempList = []
    for count in range(0, sizeOfN-1):
        tempList.append(None)
    return tempList

def construct_ngrams(sizeOfN, inputLine, padding=True):
    currentNgrams = []
    tokenized = list(inputLine)
    pad = create_NPadding(sizeOfN)
    tokenized = pad + tokenized + pad
    firstPos = 0
    secondPos = sizeOfN
    for count in range(0, len(inputLine)+sizeOfN-1):
        ngram = tokenized[firstPos:secondPos]
        currentNgrams.append(tuple(ngram))
        firstPos += 1
        secondPos += 1
    return currentNgrams

def populate_LM(lang, createdNgrams, languages):
    for tup in createdNgrams:
        for lan in languages:
            lan[tup]
        if lang == MALAY:
            languages[0][tup] += 1
        elif lang == INDONESIAN:
            languages[1][tup] += 1
        elif lang == TAMIL:
            languages[2][tup] += 1
    return languages

def handle_currentLine(currentLine, langs):
    language = extract_Language(currentLine)
    remainingLine = currentLine.split(' ', 1)[1]
    currentNgrams = construct_ngrams(NGRAM_SIZE, remainingLine)
    langs = populate_LM(language, currentNgrams, langs)
    return langs

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'
    
    # Initialise defaultdict for each language, default value is set to 1 to handle one-smoothing
    
    malaysian = defaultdict(lambda: 1)
    indonesian = defaultdict(lambda: 1)
    tamil = defaultdict(lambda: 1)
    languages = [malaysian, indonesian, tamil]
    #count = 1
    with open(in_file) as f:
        for line in f:
            languages = handle_currentLine(line, languages)
            #print count
            #count += 1
            #for l in languages:
                #print len(l)
    return languages

def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."
    # This is an empty method
    # Pls implement your code in below
    outputFile = open(out_file, 'w')
    #Reading the test file
    with open(in_file) as f:
        for line in f:
            toBeWritten = calculate_Probability(line, LM)
            outputFile.write(toBeWritten)
    outputFile.close()

def calculate_Probability(inputLine, LM):
    queryNgrams = construct_ngrams(NGRAM_SIZE, inputLine)
    unregistered_ngrams = 0 #keeps track of ngrams that are in queried line but not in training file
    #Sum of occurences of each word in trained vocabulary 
    sizeOfMalaysian = sum(LM[0].values())
    sizeOfIndonesian = sum(LM[1].values())
    sizeOfTamil = sum(LM[2].values())
    #Initialise probabilities
    probMalaysian = 0
    probIndonesian = 0
    probTamil = 0
    #Iterate through the queried ngrams and calculate probabilties for each of the langauges (using log sum to prevent underflow issue)
    for gram in queryNgrams:
        if gram in LM[0]:
            probMalaysian += log(LM[0][gram]/float(sizeOfMalaysian))
            probIndonesian += log(LM[1][gram]/float(sizeOfIndonesian))
            probTamil += log(LM[2][gram]/float(sizeOfTamil))
        else:
            unregistered_ngrams += 1
    #Creating results string
    if max(probMalaysian, probIndonesian, probTamil) == probMalaysian:
        toBeWritten = 'malaysian ' + inputLine
    elif max(probMalaysian, probIndonesian, probTamil) == probIndonesian:
        toBeWritten = 'indonesian ' + inputLine
    elif max(probMalaysian, probIndonesian, probTamil) == probTamil:
        toBeWritten = 'tamil ' + inputLine
    return toBeWritten

def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
