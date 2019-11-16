# -*- coding: utf-8 -*-
import json
import random
import re

def replace_paryavachi(sentence):
    filename = 'paryavachis.txt'
    with open(filename, 'r') as f:
        paryavachis = json.load(f)
    sentence = sentence.split(" ")
    for i, word in enumerate(sentence):
        for synset in paryavachis:
            if word in synset:
                replacement = word
                while replacement == word:
                    replacement = random.choice(synset)
                sentence[i] = replacement
    sentence = ' '.join(sentence)
    sentence = re.sub('\s+', ' ', sentence).strip()
    return sentence


def replace_vilom_shabd(sentence):
    filename = 'vilom_shabds.txt'
    with open(filename, 'r') as f:
        vilom_shabds = json.load(f)
    negative = u"नहीं"
    sentence = sentence.split(" ")
    for i, word in enumerate(sentence):
        if word in vilom_shabds.keys():
            if sentence[i+1] == negative:
                sentence[i] = random.choice(vilom_shabds[word])
                sentence[i+1] = ''
            else:
                sentence[i] = random.choice(vilom_shabds[word])+" "+negative
    sentence = ' '.join(sentence)
    sentence = re.sub('\s+', ' ', sentence).strip()
    return sentence


if __name__ == "__main__":
    print("please provide the sentance:")
    text = input()
    text1 = replace_paryavachi(text)
    print(text1)
    possible_ant = replace_vilom_shabd(text)
    print(possible_ant)
