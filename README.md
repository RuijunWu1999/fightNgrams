# Final Project: Spell Checker++
## Team Name:
N-Grams
## Team Members:
Ruijun WU

Mengyin Liu

Angelina


• List of files you are submitting and a summary of what each is for
trainer.py

Reads designed NLTK Corpus and save it as a 2-leveled dictionary.
spellchecker.py
Reads the previous saved 2-leveled dictionary , and read in a text file for the words need checked, then find the possible corrections by overlapped n-grams from the 2-leveled dictionary, rank these corrections with Levenstein Distance. Finally write out in a text file.

• List of external libraries you used and links to download anything that was not used in the homeworks

Nothing beyond given libraries.


• Description of the layout of your code

trainer.py

Level 0

Send inputs to function main after handling

Level 1 

Send inputs to function real_main and differentiate cases for arpabetmode

Level 2

Differentiate inputs by arpabetmode, using correponding sub-functions to read data and generate dictionaries, finally create Ngram dictionaries and save them in pickle files.

Level 3 

Sub-functions like reading data, creating dictionaries based on given arpahetmode, and creation of NGramsDict object

spellchecker.py

Level 0 

send inputs to main function

Level 1 

Read in Ngram dictionaries and input lines, after using sub-function to get result, write out result in output file

Level 2 

Use sub-function for each word's case and collect all words in result dictionary ]

Level 3 

Use sub-functions to generate a list of word and contents of levestein distance

Level 4 

Sub-function to get top 5 candidates with frequency greater than 40%, and another sub-function to get levestein distance

• How to run your trainer and spell checker

to Run Trainer:

corpus mode : python3 trainer.py example.pkl "Brown" -n 3

arpabetmode : python3 trainer.py example.pkl "X" --arpabetmode -n 2

to Run SpellChecker:

python3 spellchecker.py "example-tri.pkl" "testinputs.txt" "testoutputs.txt" False
The last parameter has to be FALSE, since the interactive function not implemented. 


• Which extras you implemented

4.2 N-Best 

I implemented top-5 ranked candidates and write them out to text file.

4.3 Other Corpora 

My codes can load all corpus installed.

• Any design decisions you made when implementing your code

1.You probably do not need to worry about padding, but you can if you find it reasonable. Describe your choice in your README.md.

In the process of implementing spell checking programmatically, the need for padding was not found.

2.You can fix the overlap threshold and specify it in your README.md.

I choosed 40% of overlap as the threshold.

3.ARPABET dictionary

I choosed alphabetically earlier.

4.N-Best 

I implemented top-5 ranked candidates and write them out to text file.
