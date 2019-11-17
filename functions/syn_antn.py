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
    if re.match(r".*{deletion}".format(deletion = deletion), similar):
        answer = re.sub(r"{deletion}".format(deletion = deletion), "", similar)
        original = re.sub(r"{deletion}".format(deletion = deletion), "", original)
        if original[-1] == answer[-1] or ("\u0915" <= answer[-1] <= "\u0939" and "\u0915" <= original[-1] <= "\u0939"):
            answer = answer + addition
            return answer
        else:
            return similar
    else:
        return similar


filename = 'functions/paryavachis.txt'
with open(filename, 'r') as f:
    paryavachis = json.load(f)


def replace_synonyms(senctence, word_list, original_word_list, word_count):
    paraphrases = []
    replacement_count = 0
    for i in range(word_count):
        if word_list[i].wordTag in ["NNP", "NNPC", "NNC", "VM"]:
            continue
        if word_list[i].word != original_word_list[i]:
            continue
        deletion, addition = morph(original_word_list[i], word_list[i].word)
        for synset in paryavachis:
            if original_word_list[i] in synset:
                if original_word_list[i] != word_list[i].word:
                    print("to make {} from {} add {} and delete {}".format(word_list[i].word, original_word_list[i], addition, deletion))
                for replacement in synset:
                    old = replacement
                    replacement = try_apply_morph(replacement, original_word_list[i], addition, deletion)
                    if(replacement != old):
                        print("{} can be replaced by {}".format(old, replacement))
                    if replacement != word_list[i].word:
                        paraphrases.append(copy.deepcopy(word_list))
                        paraphrases[replacement_count][i].word = replacement
                        print("replace {} ({}) with {}".format(
                            original_word_list[i], word_list[i].wordTag, replacement))
                        replacement_count += 1
                break
    return paraphrases


def replace_antonyms(senctence, word_list, original_word_list):
    pass
