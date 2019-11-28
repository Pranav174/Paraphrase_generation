import json
import copy
import re


def morph(original, inflected):
    deletion = original
    addition = inflected
    for i in range(len(original)):
        if original[:i+1] != inflected[:i+1]:
            return deletion, addition
        else:
            deletion = original[i+1:]
            addition = inflected[i+1:]
    return deletion, addition


def try_apply_morph(similar, original, addition, deletion):
    if re.match(r".*{deletion}".format(deletion=deletion), similar):
        answer = re.sub(r"{deletion}".format(deletion=deletion), "", similar)
        original = re.sub(r"{deletion}".format(
            deletion=deletion), "", original)
        if len(original) and len(answer):
            if original[-1] == answer[-1] or ("\u0915" <= answer[-1] <= "\u0939" and "\u0915" <= original[-1] <= "\u0939"):
                answer = answer + addition
                return answer
            else:
                return similar
        else:
            return similar
    else:
        return similar


filename = 'functions/paryavachis.txt'
with open(filename, 'r') as f:
    paryavachis = json.load(f)

filename = 'functions/vilom_shabds.txt'
with open(filename, 'r') as f:
    vilom_shabds = json.load(f)

negative = u"नहीं"


def replace_synonyms(sentence, word_list, original_word_list, inflected):
    paraphrases = []
    for i in sentence.wordNumList:
        if word_list[i].wordTag in ["NNP", "VM"] or word_list[i].wordTag[-1] == "C":
            continue
        if word_list[i].word == original_word_list[i] and inflected:
            continue
        if word_list[i].word != original_word_list[i] and not inflected:
            continue
        deletion, addition = morph(original_word_list[i], word_list[i].word)
        for synset in paryavachis:
            if original_word_list[i] in synset:
                if original_word_list[i] != word_list[i].word:
                    print("to make {} from {} add {} and delete {}".format(
                        word_list[i].word, original_word_list[i], addition, deletion))
                for replacement in synset:
                    old = replacement
                    replacement = try_apply_morph(
                        replacement, original_word_list[i], addition, deletion)
                    if(replacement != old):
                        print("{} can be inflected to {}".format(old, replacement))
                    if replacement != word_list[i].word:
                        paraphrases.append(
                            [word_list[word].word for word in sentence.wordNumList])
                        paraphrases[-1][i -
                                        sentence.wordNumList[0]] = replacement
                        print("replace {} ({}) with {}".format(
                            word_list[i].word, word_list[i].wordTag, replacement))
                break
    return paraphrases


def print_tree(sentence, word_list, nodeName):
    if nodeName != "None":
        node = sentence.nodeDict[nodeName]
        chunk = sentence.chunkList[node.chunkNum]
        nodeName = node.nodeParent
        print("({} {})".format(chunk.chunkTag, node.nodeRelation), end=" ")
        for word in chunk.wordNumList:
            print(word_list[word].word, end=" ")
        print()
        print_tree(sentence, word_list, nodeName)


def replace_antonyms(sentence, word_list, original_word_list, inflected):
    paraphrases = []
    for i in sentence.wordNumList:
        if word_list[i].wordTag in ["NNP"] or word_list[i].wordTag[-1] == "C":
            continue
        if word_list[i].word == original_word_list[i] and inflected:
            continue
        if word_list[i].word != original_word_list[i] and not inflected:
            continue
        if original_word_list[i] in vilom_shabds.keys():
            chunk = sentence.chunkList[word_list[i].chunkNum]
            node = sentence.nodeDict[chunk.nodeName]
            print("found {} in chunk ({} {} {})".format(
                word_list[i].word, chunk.chunkTag, chunk.nodeName, node.nodeRelation))
            # print_tree(sentence, word_list, node.nodeName)
            ccof_otw = False
            temp_node = node.nodeName
            while 1:
                if sentence.nodeDict[temp_node].nodeRelation == "ccof":
                    ccof_otw = True
                    break
                temp_node = sentence.nodeDict[temp_node].nodeParent
                if temp_node == "None":
                    break
                temp_chunk = sentence.chunkList[sentence.nodeDict[temp_node].chunkNum]
                if temp_chunk.chunkTag == "VM":
                    break

            if ccof_otw or temp_node == "None":
                continue
            deletion, addition = morph(original_word_list[i], word_list[i].word)
            chunk_to_edit = sentence.chunkList[sentence.nodeDict[temp_node].chunkNum]
            already_negative = 0
            print("will edit : ", end="")
            for word in chunk_to_edit.wordNumList:
                if word_list[word].word == negative:
                    already_negative = word
                print(word_list[word].word, end=" ")
            print()

            for replacement in vilom_shabds[original_word_list[i]]:
                old = replacement
                replacement = try_apply_morph(replacement, original_word_list[i], addition, deletion)
                if(replacement != old):
                    print("{} can be inflected to {}".format(old, replacement))
                paraphrases.append([word_list[word].word for word in sentence.wordNumList])
                paraphrases[-1][i - sentence.wordNumList[0]] = replacement
                if already_negative:
                    del paraphrases[-1][already_negative - sentence.wordNumList[0]]
                else:
                    paraphrases[-1].insert(chunk_to_edit.wordNumList[0] - sentence.wordNumList[0], negative)
                print("replace {} ({}) with {}".format(
                    original_word_list[i], word_list[i].wordTag, replacement))
    return paraphrases
