import copy
import random 
import re 
class Tree(object):
    def __init__(self):
        self.left = []
        self.right = []
        self.text = ""
        self.chunkNum = -1


def re_arrange(sentence, word_list):
    sentence = copy.deepcopy(sentence)

    while(1):
        found = False
        for tag in sentence.nodeDict.keys():
            # if sentence.nodeDict[tag].nodeRelation == "k2":
            if sentence.nodeDict[tag].nodeRelation == "k2" and word_list[sentence.chunkList[sentence.nodeDict[tag].chunkNum].wordNumList[0]].word == u'कि':
                word_list[sentence.chunkList[sentence.nodeDict[tag].chunkNum].wordNumList[0]].word = ""
                found=True
                break
            if sentence.nodeDict[tag].nodeRelation == "fragof" and sentence.nodeDict[tag].chunkNum!=-1:
                merge_nodes(tag, sentence.nodeDict[tag].nodeParent, sentence, word_list)
                found=True
                break
            if sentence.nodeDict[tag].nodeRelation == "pof" and sentence.nodeDict[tag].chunkNum!=-1:
                merge_nodes(tag, sentence.nodeDict[tag].nodeParent, sentence, word_list)
                found=True
                break
        if not found:
            break

    if replace_blk_root(sentence, word_list):
        print_sentence(sentence, word_list)
        print_dependency(sentence, word_list)
        root_node = 0
        for tag in sentence.nodeDict.keys():
            if sentence.nodeDict[tag].nodeParent == "None":
                root_node = tag
                break
        tree = build_tree(sentence,word_list,sentence.nodeDict[root_node].chunkNum)
        print("tree_built")
        print_tree(tree, -1)
        paraphrases = []
        for i in range(5):
            paraphrases.append(generate_random_paraphrase(tree).split(" "))
        return paraphrases
    else:
        return []


def replace_blk_root(sentence, word_list):
    blk_node = 0
    root_node = 0
    blk_node = sentence.chunkList[word_list[sentence.wordNumList[-1]].chunkNum].nodeName
    if sentence.nodeDict[blk_node].nodeRelation != "rsym":
        blk_node = 0
    # for chunk in sentence.chunkList:
    #     if chunk.chunkTag == "BLK":
    #         blk_node = chunk.nodeName
    #         break
    for tag in sentence.nodeDict.keys():
        if sentence.nodeDict[tag].nodeParent == "None":
            root_node = tag
            break
    if not blk_node or not root_node:
        return 0

    blk_chunk = sentence.nodeDict[blk_node].chunkNum
    root_chunk = sentence.nodeDict[root_node].chunkNum

    sentence.chunkList[blk_chunk].nodeName = root_node
    sentence.chunkList[root_chunk].nodeName = blk_node

    sentence.nodeDict[blk_node].chunkNum = root_chunk
    sentence.nodeDict[root_node].chunkNum = blk_chunk

    return 1

def print_sentence(sentence, word_list):
    print("sentence: ", end="")
    for word in sentence.wordNumList:
        print(word_list[word].word, end=" ")
    print()

def merge_nodes(node2, node1, sentence, word_list):
    # print("Asking to merge {} and {}".format(node1, node2))
    node1_chunk = sentence.nodeDict[node1].chunkNum
    node2_chunk = sentence.nodeDict[node2].chunkNum
    # print("{} {}".format(node1_chunk,node2_chunk))
    # print_sentence(sentence, word_list)
    # print_dependency(sentence, word_list)

    if node1_chunk < node2_chunk:
        for chunk in range(node1_chunk+1, node2_chunk+1):
            sentence.chunkList[node1_chunk].wordNumList.extend(sentence.chunkList[chunk].wordNumList)
            sentence.nodeDict[sentence.chunkList[node1_chunk].nodeName].childList.extend(sentence.nodeDict[sentence.chunkList[chunk].nodeName].childList)
            for child in sentence.nodeDict[sentence.chunkList[chunk].nodeName].childList:
                sentence.nodeDict[child].nodeParent = node1
            sentence.nodeDict[sentence.chunkList[chunk].nodeName].chunkNum=-1
    else:
        numlist=[]
        for chunk in range(node2_chunk, node1_chunk+1):
            numlist.extend(sentence.chunkList[chunk].wordNumList)
        sentence.chunkList[node1_chunk].wordNumList = numlist
        for chunk in range(node2_chunk, node1_chunk):
            sentence.nodeDict[sentence.chunkList[node1_chunk].nodeName].childList.extend(sentence.nodeDict[sentence.chunkList[chunk].nodeName].childList)
            for child in sentence.nodeDict[sentence.chunkList[chunk].nodeName].childList:
                sentence.nodeDict[child].nodeParent = node1
            sentence.nodeDict[sentence.chunkList[chunk].nodeName].chunkNum=-1

    # print_dependency(sentence, word_list)
    # print_sentence(sentence,word_list)
    # print()

def print_dependency(sentence, word_list):
    print_sentence
    ori = ['None']
    next = []
    while 1:
        for tag in sentence.nodeDict.keys():
            # print(tag, '  ' , sentence.nodeDict[tag].__dict__)
            if sentence.nodeDict[tag].nodeParent in ori and sentence.nodeDict[tag].chunkNum != -1:
                next.append(tag)
        if len(next):
            for node in next:
                print(node, "(", end="")
                # print(sentence.chunkList[sentence.nodeDict[node].chunkNum].__dict__, end="")
                for i,num in enumerate(sentence.chunkList[sentence.nodeDict[node].chunkNum].wordNumList):
                    if i!=0:
                        print("", word_list[num].word, end="")
                    else:
                        print(word_list[num].word, end="")
                print(")", end=" ")
                for child in sentence.nodeDict[node].childList:
                    print(sentence.nodeDict[child].nodeName, end=" ")
                print(")" , sentence.nodeDict[node].nodeRelation, sentence.nodeDict[node].nodeParent, end="\t\t")
            print()
            ori = next
            next = []
        else:
            break
    print()


def build_tree(sentence, word_list, chunkNum):
    temp = Tree()
    temp.chunkNum = chunkNum
    for word in sentence.chunkList[chunkNum].wordNumList:
        temp.text += " " + word_list[word].word
    # print("{} {}".format(temp.chunkNum, temp.text))
    node = sentence.chunkList[chunkNum].nodeName
    for child in sentence.nodeDict[node].childList:
        if sentence.nodeDict[child].chunkNum < 0:
            continue
        if sentence.nodeDict[child].chunkNum < chunkNum:
            temp.left.append(build_tree(sentence, word_list, sentence.nodeDict[child].chunkNum))
        else:
            temp.right.append(build_tree(sentence, word_list, sentence.nodeDict[child].chunkNum))
    return temp

def print_tree(n, parent):
    for child in n.left:
        print_tree(child,n.chunkNum)
    print("{} ({}) {}".format(n.chunkNum, n.text, parent))
    for child in n.right:
        print_tree(child,n.chunkNum)


def generate_random_paraphrase(tree):
    random.shuffle(tree.left)
    random.shuffle(tree.right)
    text=""
    for x in tree.left:
        text += " " + generate_random_paraphrase(x)
    text += " " + tree.text
    for x in tree.right:
        text += " " + generate_random_paraphrase(x)
    text = re.sub(' +', ' ', text)
    return text.strip()
    
