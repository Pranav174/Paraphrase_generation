import pickle
import os
from ssf_api import *

from functions.syn_antn import replace_synonyms, replace_antonyms
from functions.re_arrange import re_arrange
from functions.active_to_passive import kritvachya_to_karmvachya

loli= 1
for f in os.listdir("DATA/PROCESSED-DATA/collection/"):
    loli +=1
    if loli>50:
        break
    ofile = open("DATA/PROCESSED-DATA/collection/" + f,"rb")
    var = pickle.load(ofile)

    originals = []
    for i in var.globalWordList:
        try:
            originals.append(i.featureSet.featureDict['af'].split(',')[0])
        except:
            originals.append(i.word)

    for sentence in var.sentenceList:
        # answer = replace_antonyms(sentence, var.globalWordList, originals, False)
        # answer = replace_antonyms(sentence, var.globalWordList, originals, True)
        # answer = replace_synonyms(sentence, var.globalWordList, originals, False)
        # answer = replace_synonyms(sentence, var.globalWordList, originals, True)
        # answer = re_arrange(sentence, var.globalWordList)
        answer = kritvachya_to_karmvachya(sentence, var.globalWordList, originals)
        if len(answer):
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


