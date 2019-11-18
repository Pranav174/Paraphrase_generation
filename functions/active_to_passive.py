from functions.re_arrange import print_dependency,print_sentence
import copy
import sys
import re


def kritvachya_to_karmvachya(sentence,word_list,original):
    paraphrases = []
    # print()
    # print_sentence(sentence,word_list)
    possible = nodes_possible_to_be_changed(sentence,word_list,original)
    for poss in possible:
        print(poss)
        new_sentence = copy.deepcopy(sentence)
        new_wordlist = copy.deepcopy(word_list)
        # for word in new_sentence.chunkList[new_sentence.nodeDict[poss[1]].chunkNum].wordNumList:
            # print("checking {}".format(new_wordlist[word].word))
        for word in reversed(new_sentence.chunkList[new_sentence.nodeDict[poss[1]].chunkNum].wordNumList):
            if new_wordlist[word].wordTag == 'PSP':
                new_wordlist[word].word = ""
            else:
                if new_wordlist[word].wordTag != 'RP':
                    if new_wordlist[word].wordTag == 'PRP':
                        if original[word] in prp_replacement.keys():
                            new_wordlist[word].word = prp_replacement[original[word]]
                    new_wordlist[word].word += " द्वारा"
                    break
        for word in new_sentence.chunkList[new_sentence.nodeDict[poss[2]].chunkNum].wordNumList:   
            if new_wordlist[word].wordTag == 'PSP':
                new_wordlist[word].word = ""
        main_verb = 0
        for word in reversed(new_sentence.chunkList[new_sentence.nodeDict[poss[0]].chunkNum].wordNumList):
            # print("checking {} {}".format(new_wordlist[word].word, new_wordlist[word].word[0]))
            if new_wordlist[word].wordTag != 'VAUX' or original[word] not in ['है','रह', 'था', 'हैं', 'रहा']:
            # if new_wordlist[word].wordTag != 'VAUX' or new_wordlist[word].word[0] not in ['ह','र', 'थ']:
                if new_wordlist[word].wordTag not in ['SYM', 'NEG']:
                    if original[word] != 'जा':
                        main_verb=word
                        break
        if main_verb:
            sb = samanya_bhootkal(original[main_verb], new_wordlist[main_verb].featureSet.featureDict['af'].split(',')[-1])
            if sb:
                new_wordlist[main_verb].word = sb
                k2_gender = "m"
                for word in new_sentence.chunkList[new_sentence.nodeDict[poss[2]].chunkNum].wordNumList:
                    if "head" in new_wordlist[word].featureSet.featureDict['chunktype']:
                        k2_gender = new_wordlist[word].featureSet.featureDict['af'].split(',')[2]
                from_matra = "ी"
                to_matra = "ा"
                if k2_gender == 'f':
                    from_matra,to_matra=to_matra,from_matra
                for word in new_sentence.chunkList[new_sentence.nodeDict[poss[0]].chunkNum].wordNumList:
                    if new_wordlist[word].wordTag not in ['SYM', 'NEG'] and new_wordlist[word].word != "जा":
                        temp = new_wordlist[word].word.split(" ")
                        for i,temp_word in enumerate(temp):
                            if temp_word[-1] == from_matra:
                                temp[i] = temp_word[:-1]+to_matra
                        new_wordlist[word].word = " ".join(temp)

                # new_wordlist[main_verb].word += " " + replacement[new_wordlist[main_verb].featureSet.featureDict['af'].split(',')[-1]]
                print_dependency(new_sentence,new_wordlist)
                paraphrases.append([re.sub(' +', ' ',new_wordlist[word].word.strip()) for word in sentence.wordNumList if new_wordlist[word].word!=""])
    
    # if len(possible):
    #     proper_list(sentence,word_list)
    #     print_dependency(sentence, word_list)
    return paraphrases

def nodes_possible_to_be_changed(sentence, word_list, original):
    possible = []
    for tags in sentence.nodeDict.keys():
        if "VGF" in tags and not ((original[sentence.chunkList[sentence.nodeDict[tags].chunkNum].wordNumList[0]] in ["हैं", "है", "था"]) or sentence.nodeDict[tags].chunkNum == -1):
            k1 = 0
            k2 = 0
            for child in sentence.nodeDict[tags].childList:
                if sentence.nodeDict[child].nodeRelation == 'k1' and "NP" in child:
                    k1 = child
                if sentence.nodeDict[child].nodeRelation == 'k2':
                    k2 = child
            if k1 and k2:
                try:
                    if word_list[sentence.chunkList[sentence.nodeDict[tags].chunkNum].wordNumList[0]].featureSet.featureDict['voicetype'] == 'active':           
                        possible.append([tags,k1,k2])
                except:
                    continue
    return possible

def proper_list(sentence, word_list):
    for word in sentence.wordNumList:
        print(word_list[word].word, end=" ")
        # print(word_list[word].chunkNum, end=" ")
        try:
            print("({})".format(word_list[word].featureSet.featureDict), end=" ")
        except:
            pass
        print(word_list[word].wordTag)

replacement = {
    "yA" : "गया",
    "nA" : "जाना",
    "gA" : "जाएगा",
    "wA" : "जाता",
    "eM" : "जाए",
    "0" : "जा",
    "aO" : "जाओ"
}

prp_replacement = {
    "वह" : "उनके",
    "कोई" : "किसीके",
    "यह" : "इसके",
    "खुद" : "खुदके",
    "हम" : "हमारे",
    "मैं" : "मेरे"
}

def samanya_bhootkal(word, ja_form):
    if "\u0915" <= word[-1] <= "\u0939":
        word += u'ा'
    else:
        word += u'या'
    try:
        word+=" " + replacement[ja_form]
    except:
        return None
        # sys.stderr.write(ja_form+ '\n')
        # print("blabla")
        
    # print(ja_form)

    return word
