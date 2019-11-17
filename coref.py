import pickle
import os
from ssf_api import *

from functions.syn_antn import replace_synonyms, replace_antonyms

loli= 1
for f in os.listdir("DATA/PROCESSED-DATA/collection/"):
    loli +=1
    if loli>30:
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
        # start = sentence.wordNumList[0]
        # end = sentence.wordNumList[-1]+1
        answer = replace_antonyms(sentence, var.globalWordList, originals, False)
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



    # for sentence in var.sentenceList:
    #     count = 0
    #     for tag in sentence.nodeDict.keys():
    #         if sentence.nodeDict[tag].nodeParent == 'None' and sentence.nodeDict[tag].chunkNum != -1:
    #             count+=1
    #     if count>1:
    #         print(count)
    #         print("SENTENCE:")
    #         for word in sentence.wordNumList:
    #             print(var.globalWordList[word].word, end=" ")
    #         print()
    #         for word in sentence.wordNumList:
    #             print(var.globalWordList[word].featureSet.__dict__)
    #         print()
    #         print(sentence.__dict__)
    #         print("nodes:")
    #         for tag in sentence.nodeDict.keys():
    #             print(tag, '  ' , sentence.nodeDict[tag].__dict__)
    #             # print(tag)
    #         print("chunks")
    #         for chunk in sentence.chunkList:
    #             print(chunk.__dict__)
    #         for root in sentence.rootNode:
    #             print(root)
    #         print()

    # print("\n")


