from __future__ import division
import pickle
import sys
import os
from ssf_api import *


loli= 1
for f in os.listdir("DATA/PROCESSED-DATA/collection/"):
    loli +=1
    if loli>300:
        break
    ofile = open("DATA/PROCESSED-DATA/collection/" + f,"rb")
    var = pickle.load(ofile)

    originals = []
    for i in var.globalWordList:
        try:
            originals.append(i.featureSet.featureDict['af'].split(',')[0])
        except:
            originals.append(i.word)
        print(i.word, originals[-1])



    for sentence in var.sentenceList:
        count = 0
        for tag in sentence.nodeDict.keys():
            if sentence.nodeDict[tag].nodeParent == 'None' and sentence.nodeDict[tag].chunkNum != -1:
                count+=1
        if count>1:
            print(count)
            print("SENTENCE:")
            for word in sentence.wordNumList:
                print(var.globalWordList[word].word, end=" ")
            print()
            for word in sentence.wordNumList:
                print(var.globalWordList[word].featureSet.__dict__)
            print()
            print(sentence.__dict__)
            print("nodes:")
            for tag in sentence.nodeDict.keys():
                print(tag, '  ' , sentence.nodeDict[tag].__dict__)
                # print(tag)
            print("chunks")
            for chunk in sentence.chunkList:
                print(chunk.__dict__)
            for root in sentence.rootNode:
                print(root)
            print()

    # print("\n")


