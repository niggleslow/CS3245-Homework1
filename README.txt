This is the README file for A0110574N's submission

== General Notes about this assignment ==

For this assignment, the general outline of the code is as follows:

1. Create dictionaries for each of the 3 languages
2. To handle the issue of one-smoothing, each language is initialised as a defaultdict with the default value set to 1.
3. When parsing each line of the training data, the origin language is extracted first. Subsequently, padding and splitting the remaining lines into a list of ngrams is carried out.
4. During the calculation of probability phase, additive logarithmic is carried out on the probabilities of the ngrams instead of simply multiplying them in order to minimize the risk of possible underflow.
5. Furthermore, a counter is maintained in order to keep track of the number of unregistered ngrams from the test data given. Afterwhich, if the ratio of the number of unregistered ngrams to total ngrams exceeds a pre-determined ratio, the language for that line is determined to be of 'other' type.
6. If it is not determined to be of 'other' type, the highest value amongst the additive log results will then determine the type of language of the test data line.

As the program is meant to be customizable, the default values are:

padding = TRUE - left/right padding enabled
charTok = TRUE - character tokenizing enabled, if set to false, token-based tokenizing is enabled
OTHER_THRESHOLD = 0.5 - threshold ratio for which a language is determined to be 'other' or not
NGRAM_SIZE = 4 - size of ngrams is default to 4 characters per ngram

== Files included with this submission ==

build_test_LM.py - source code for the assignment
README.txt - information about the overall assignment
ESSAY.txt - answers to the essay questions

== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0110574N, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

-NA-

I suggest that I should be graded as follows:

-NA-

== References ==

https://www.accelebrate.com/blog/using-defaultdict-python/ - Provided idea to use default dictionary to solve one-smoothing problem
https://www.python.org/ - Provided clarification of Python syntax (Been a while since I last used Python to code)