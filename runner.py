import pickle
import os, sys, getopt
from ssf_api import *

from functions.syn_antn import replace_synonyms, replace_antonyms
from functions.re_arrange import re_arrange
from functions.active_to_passive import kritvachya_to_karmvachya

def generate_paraphrases(option, count):
    if 1 <= option <= 6:
        paraphrased = 0
        totat_paraphrased = 0
        for f in os.listdir("DATA/PROCESSED-DATA/collection/"):
            ofile = open("DATA/PROCESSED-DATA/collection/" + f,"rb")
            var = pickle.load(ofile)

            originals = []
            for i in var.globalWordList:
                try:
                    originals.append(i.featureSet.featureDict['af'].split(',')[0])
                except:
                    originals.append(i.word)

            for sentence in var.sentenceList:
                answer=[]
                if option == 1:
                    answer = replace_synonyms(sentence, var.globalWordList, originals, False)
                if option == 2:
                    answer = replace_synonyms(sentence, var.globalWordList, originals, True)
                if option == 3:
                    answer = replace_antonyms(sentence, var.globalWordList, originals, False)
                if option == 4:
                    answer = replace_antonyms(sentence, var.globalWordList, originals, True)
                if option == 5:
                    answer = re_arrange(sentence, var.globalWordList)
                if option == 6:
                    answer = kritvachya_to_karmvachya(sentence, var.globalWordList, originals)
                
                if len(answer):
                    totat_paraphrased +=1
                    print("original: ")
                    for word in sentence.wordNumList:
                        print(var.globalWordList[word].word, end=" ")
                    print()
                for i,paraphrase in enumerate(answer):
                    print(i,":")
                    for word in paraphrase:
                        print(word, end=" ")
                    print()
                if len(answer):
                    print()

            paraphrased +=1
            if paraphrased > count:
                break

        print("Total paraphrased = {}".format(totat_paraphrased))

    else:
        print("Valip options 1-6")


def print_options():
    print('EXPECTED: runner.py -o <option> (-n <number_of_articles_to_parse>)\nOPTIONS:')
    print("  1: Synonym replacement")
    print("  2: Synonym replacement (inflected base form)")
    print("  3: Antonym replacement")
    print("  4: Antonym replacement (inflected base form)")
    print("  5: Reorder chunks")
    print("  6: Active to Passive")
    

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"o:n:",["option=", "number="])
    except getopt.GetoptError:
        print_options()
        sys.exit(2)
    option = 0
    number = 50
    for opt, arg in opts:
        if opt in ("-o", "--option"):
            option = int(arg)
        if opt in ("-n", "--number"):
            number = int(arg)
    if option:
        generate_paraphrases(option,number)
    else:
        print_options()

if __name__ == "__main__":
   main(sys.argv[1:])