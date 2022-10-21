import sys
import argparse
import nltk
import pickle
# IMPORT MORE LIBRARIES HERE
# IF you create other .py files, IMPORT THEM HERE
import trainer
NGramsDict = trainer.NGramsDict
# Need this line to make pickle recognize the imported CLASS

# ADD YOUR FUNCTIONS HERE
def tempMain1():
    # Two test cases.
    main("example-tri.pkl", "testinputs.txt", "testoutputs.txt", False)
    main("example-arpa.pkl", "arpa-testinputs.txt", "arpa-testoutputs.txt", True)
    return


def findTopKCandidates(newNgrams, trainNGramsDict):
    allCandidates = []
    targetMatches = len(newNgrams)*0.4
    # Look for at least 40% matches of ngram
    for eachNgram in newNgrams:
        prevSet = set()
        prevSet.update(trainNGramsDict.ngramdict.get(eachNgram, []))
        # get all trained words of sub-dictionary with ngram as KEY for each case, list is also applicable

        for eachWord in prevSet:
            if eachWord not in allCandidates:
            # Process words that aren't in the python list "allCandicates" yet
                ngrams = nltk.ngrams(eachWord, trainNGramsDict.ngramtype)
                matchedNgrams = sum((1 for ngram in ngrams if ngram in newNgrams))
                # count matched ngrams between target and trained word
                allCandidates.append((eachWord, matchedNgrams))

        result = [x[0] for x in sorted(allCandidates, key=lambda x:x[1], reverse = True) if x[1] >= targetMatches]
        # sort results in allCandidates order bt decending order, then filtering those with contents passed requirement (targetMatches)
    return result


# From Levenshtein wiki, transitioned from C++ version
def LevenshteinDistanceTwoRows(s,t):
    # Corrected Python3 Version
    #// create two work vectors of integer distances
    m = len(s)
    n = len(t)
    max_m = max(m, n)
    v0 =[x for x in range(max_m+1)]
    v1 =[0 for x in range(max_m+1)]

    for i in range( m ):
        # java, python index starts from 0, and m not included.
        #// calculate v1 (current row distances) from the previous row v0
        #// first element of v1 is A[i + 1][0]
        #// edit distance is last element of v0,
        #// edit distance is delete (i + 1) chars from s to match empty t
        v1[0] = i + 1

        # // use formula to fill in the rest of the row
        for j in range( n ):
            #// calculating costs for A[i + 1][j + 1]
            deletionCost = v0[j + 1] + 1
            insertionCost = v1[j] + 1
            if s[i] == t[j]:
                substitutionCost = v0[j]
            else:
                substitutionCost = v0[j] + 1
            v1[j + 1] = min(deletionCost, insertionCost, substitutionCost)

        #// copy v1 (current row) to v0 (previous row) for next iteration
        #// since data in v1 is always invalidated, a swap without copy could be more efficient
        v0 = v1[:]
    return v0[n]


def trainedsc_correct_word(targetWord, trainNGramsDict):
    if not trainNGramsDict.arpabetmode:
        # Normal mode, lower case all words.
        newNgrams = list(nltk.ngrams(targetWord.lower(), trainNGramsDict.ngramtype))
    else:
        newNgrams = list(nltk.ngrams(targetWord, trainNGramsDict.ngramtype))

    if newNgrams[0] in trainNGramsDict.ngramdict and targetWord in trainNGramsDict.ngramdict[newNgrams[0]]:
        # The target word exists in dictionary, no need to check spelling.
        return [(targetWord, 0)]
        # return as tuple in list.
    else:
        topK = findTopKCandidates(newNgrams, trainNGramsDict)
        if len(topK) == 0:
            # Completely no matched.
            result = []
        else:
            lev_dist_dict = {}
            for eachWord in topK:
                # calculate Levenshtain Distatnce and save to a temp dict.
                lev_dist = LevenshteinDistanceTwoRows(targetWord, eachWord)
                lev_dist_dict[eachWord] = lev_dist
            bestDist = min(lev_dist_dict.values())
            result = [(k,v) for k,v in lev_dist_dict.items() if v <= (bestDist+2)]
            # filter out Lev_dist > min+2
            if len(result) < 5:
                result = sorted(((k,v) for k,v in lev_dist_dict.items()),
                                key=lambda x:x[1])[:min(5, len(lev_dist_dict))]
                # sort in ascending order
                # if results number less than 5, try take results from lev_dist_dict up to 5 at least.
            else:
                result = sorted(result, key=lambda x:x[1])
                # sort in ascending order
            # return as tuple in list.

    return result


def trainedsc_correct(toBeSpellChecked, trainNGramsDict):
    result = {}
    for eachWord in toBeSpellChecked:
        result[eachWord] = trainedsc_correct_word(eachWord, trainNGramsDict)
    return result


def main(modelfname, inputfname, outputfname, interactive): # YOU CAN ADD ADDITIONAL ARGUMENTS HERE
    #DELETE THIS AND ADD YOUR OWN CODE
    print("Read model from %s" % modelfname)
    print("Spellcheck file %s" % inputfname)
    print("Write output to file %s" % outputfname)
    if interactive:
        print("In interactive mode mode")

    with open(modelfname, 'rb') as fin:
        trainNGramsDict = pickle.load(fin)

    with open(inputfname, "r") as fin:
        inputLines = fin.readlines()

    if trainNGramsDict.arpabetmode:
        toBeSpellChecked = [tuple(eachLine.split()) for eachLine in inputLines]
    else:
        toBeSpellChecked = [eachWord for wordList in [eachLine.lower().split() for eachLine in inputLines] for eachWord in wordList]

    correctedResult = trainedsc_correct(toBeSpellChecked, trainNGramsDict)

    with open(outputfname, 'w') as fout:
        if not trainNGramsDict.arpabetmode:
            for eachWord in correctedResult:
                line0 = eachWord + " ==> "
                line1 = [ str(x) for x in correctedResult[eachWord]]
                # convert tuple to str.
                line1 = " ; ".join(line1)
                fout.writelines(line0 + line1 + "\n")
        else:
            for eachWord in correctedResult:
                line0 = str(eachWord) + " ==> "
                line1 = [str(x) for x in correctedResult[eachWord]]
                line1 = " ; ".join(line1)
                fout.writelines(line0 + line1 + "\n")
    return


if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Train a Spellchecker")
    parser.add_argument("modelfname", help="file path to pickle file to read the trained spell checker model from")
    parser.add_argument("inputfname", help="File to spell check")
    parser.add_argument("outputfname", help="File to save corrected output to")
    parser.add_argument("--interactive", help="Run in interactive mode (if implemented)", action="store_true")
    ### YOU CAN ADD ADDITIONAL ARGUMENTS HERE


    args = parser.parse_args()

    main(args.modelfname, args.inputfname, args.outputfname, args.interactive) # YOU CAN ADD ADDITIONAL ARGUMENTS HERE
    #tempMain1()