import sys
import argparse
import pickle
# IMPORT MORE LIBRARIES HERE
import nltk.corpus

# IF you create other .py files, IMPORT THEM HERE


class NGramsDict(object):
    """Object representing a ngrams dictionary."""
    # to be saved into pickle library format
    def __init__(self, corpustype, ngramtype, arpabetmode, ngramdict):
        self.corpustype = corpustype
        self.ngramtype = ngramtype
        self.arpabetmode = arpabetmode
        self.ngramdict = ngramdict


# ADD YOUR FUNCTIONS HERE
def real_main(modelfname, corpustype, ngramtype, arpabetmode):
    if not arpabetmode:
    # normal mode, to read NLTK Carpus
        words = read_Corpus(corpustype)
        ngr_dict = gen_ngrams_Dict(ngramtype, words)
    else:
        print("Loading in ARPABET mode with CMUDict.")
        transcriptions = [transc for word, transc in nltk.corpus.cmudict.entries()]
        ngr_dict = gen_arpabet_ngrams_Dict(ngramtype, transcriptions)

    new_Dict = NGramsDict(corpustype, ngramtype, arpabetmode, ngr_dict)
    # wb: write in binary
    with open(modelfname, "wb") as fout:
        pickle.dump(new_Dict, fout)
    print("Trained Model saved as : %s" % modelfname)
    return


def gen_arpabet_ngrams_Dict(ngramtype, transcriptions):
    n_g_dict = {}
    for w in transcriptions:
        # if need padded:
        # padded = nltk.pad_sequence(w, ngramtype, pad_left=False,
        #                           pad_right=False,
        #                           left_pad_symbol=START,
        #                           right_pad_symbol=STOP)
        new_ngrams = list(nltk.ngrams(w, ngramtype))
        for k in new_ngrams:
            if k not in n_g_dict:
                n_g_dict[k] = set()
                n_g_dict[k].add(tuple(w))
                # put tupled ngrams into set structure
            else:
                n_g_dict[k].add(tuple(w))
    return n_g_dict


def gen_ngrams_Dict(ngramtype, words):
    n_g_dict = {}
    for w in words:
        # if need padded:
        # padded = nltk.pad_sequence(w, ngramtype, pad_left=False,
        #                           pad_right=False,
        #                           left_pad_symbol=START,
        #                           right_pad_symbol=STOP)
        w = w.lower()
        # Need to lower it for spell checking efficiency
        new_ngrams = list(nltk.ngrams(w, ngramtype))
        for k in new_ngrams:
            if k not in n_g_dict:
                n_g_dict[k] = set()
                n_g_dict[k].add(w)
                # put tupled ngrams into set structure
            else:
                n_g_dict[k].add(w)
    return n_g_dict


def read_Corpus(corpustype):
    print("Loading with %s corpus" % corpustype)
    import os
    all_installed_corpus = os.listdir(nltk.data.find("corpora"))
    # load all corpus names into list
    if corpustype.lower() not in all_installed_corpus:
        print("Corpus %s not found: " % corpustype)
        print("Please verify that the corpus installed.")
        exit(-1)
        # exit with error number -1
    # as long as the corpus package installed, getattr will load it
    mycorpus = nltk.corpus.__getattr__(corpustype.lower())
    words = mycorpus.words()
    return words


def temp_main1():
    main("example-tri.pkl", "Brown", 3, False)
    # equals to : python3 trainer.py example.pkl -n 3

    main("example-arpa.pkl", "Brown", 2, True)
    # equals to : python3 trainer.py example.pkl --arpabetmode -n 2
    return


def main(modelfname, corpustype, ngramtype, arpabetmode): # YOU CAN ADD ADDITIONAL ARGUMENTS HERE
    print("Will write model to %s" % modelfname)
    print("Using %s-grams" % ngramtype)
    if arpabetmode:
        print("In ARPABET mode")
    else:
        print("Training on %s corpus" % corpustype)

    real_main(modelfname, corpustype, ngramtype, arpabetmode)
    # call the real processing subroutine.
    return


if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Train a Spellchecker")
    parser.add_argument("modelfname", help="file path to pickle file to write the trained spell checker model to")
    parser.add_argument("-c", "--corpustype", help="Specifies training corpus. Defaults to Brown if argument is omitted. If the corpus name is unrecognized, the program immediately exists", default="Brown")
    parser.add_argument("-n", "--ngramtype", help="type of ngram to use in the overlap dictionary. Expects an int")
    parser.add_argument("--arpabetmode", help="ignore corpus type argument. Loads the CMUDict and runs in arpabet mode instead.", action="store_true")
    ### YOU CAN ADD ADDITIONAL ARGUMENTS HERE


    args = parser.parse_args()

    main(args.modelfname, args.corpustype, args.ngramtype, args.arpabetmode) # YOU CAN ADD ADDITIONAL ARGUMENTS HERE
    #temp_main1()
