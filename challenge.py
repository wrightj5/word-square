import os, sys, itertools
from collections import defaultdict
global dicti
done1 = {}


## Class def of the Tree - extends defaultdict
class Tree(defaultdict):
    def __init__(self, value=None):
        super(Tree, self).__init__(Tree)
        self.value = value
        
dicti = {}
## Had scoping problems. This ensures we only have 1 tree
def save_tree(name, tree):
    dicti[name] = tree

## Build a tree for lookahead search
## Tree is like so:
## {WORD = word}, {0 : {W : { WORD} }, {1 : {O : { WORD} },{2 : {R : { WORD} },{3 : {D : { WORD} }
def get_tree(length):
    ## Could put this in a loop to generate them
    new_dict = {}
    new_dict[0] = {}
    new_dict[1] = {}
    new_dict[2] = {}
    new_dict[3] = {}
    new_dict[4] = {}
    new_dict[5] = {}
    new_dict[6] = {}
    new_dict[7] = {}
    for d in dicti.iteritems():
        for num in range(0,length):
            position = d[1].items()[num][0]
            char = d[1].items()[num][1].items()[0][0]
            value = d[1].items()[num][1].items()[0][1]
            try:
                if char in new_dict[position]:
                    tmp = new_dict[position][char]
                    tmp.append(value)
                    new_dict[position][char] = tmp
                else:
                    new_dict[position][char] = [value]
            except:
                pass
    return new_dict

## Generate a word list which gets each word that is of size N (size of grid)
def wordlist(length, input, sourcefile="/usr/share/dict/words"):
    input = sorted(input)
    word_list = []   
    sourcefileobj = open(sourcefile)
    with open(sourcefile,'r') as f:
        for line in f:
            if(len(line.strip()) == length):
                if enough_letters(input, line.strip()):
                    word_list.append(line.strip())
    return word_list

def wordgen(word_list, input, length):
    print("Generating Tree")
    for word in word_list:
        prefix_dict = Tree()
        for pos in range(0, length):
            if pos in prefix_dict.keys():
                prefix_dict[pos][word[pos].strip()].append(word.strip())
            else:
                prefix_dict[pos][word[pos].strip()] = word.strip()
            save_tree(word.strip(), prefix_dict)
    return word_list, get_tree(length)
  

## If this was production code - i'd make this a lambda function and call it recursively. For now - this does the trick.
def generategrid4(step2dict, length, prefix_dict, input):
    for word1 in step2dict:  ## for each word
        try: ## To grab key errors
            for word2 in prefix_dict[0][word1[1]]:  ## get the 2nd words associated
                for word3 in prefix_dict[0][word1[2]]: ## Lookahead in the tree to select a suitable word
                    if word3[1] == word2[2]: ## ensure the 2nd letter in word 3 is the same as the 3rd in word 2
                        for word4 in zip(prefix_dict[0][word1[3]], prefix_dict[1][word2[3]],prefix_dict[2][word3[3]]): ## More of the same now, repeats for each n (n being the grid size)
                            for w4 in word4:
                                if(w4[0] == word1[3] and w4[1] == word2[3] and w4[2] == word3[3]):
                                    if length == 4: ## FOUR
                                        str = check_letters( input, length, word1, word2, word3, w4)
                                        if str: print str; return
                                    else:  ## Anything greater than 4
                                        for word5 in zip(prefix_dict[0][word1[4]], prefix_dict[1][word2[4]],prefix_dict[2][word3[4]], prefix_dict[3][w4[4]]):
                                            for w5 in word5:
                                                if(w5[0] == word1[4] and w5[1] == word2[4] and w5[2] == word3[4] and w5[3] == w4[4]):
                                                    if length == 5: ## FIVE
                                                        str = check_letters(input, length, word1, word2, word3,  w4, w5)
                                                        if str: print str; return                                                
                                                    else:  ## Anything greater than 5
                                                        for word6 in zip(prefix_dict[0][word1[5]], prefix_dict[1][word2[5]],prefix_dict[2][word3[5]], prefix_dict[3][w4[5]], prefix_dict[4][w5[5]]):
                                                            for w6 in word6:
                                                                if(w6[0] == word1[5] and w6[1] == word2[5] and w6[2] == word3[5] and w6[3] == w4[5] and w6[4] == w5[5]):
                                                                    if length == 6: ## SIX
                                                                        str = check_letters(input, length, word1, word2, word3,  w4, w5, w6)
                                                                        if str: print str; return
                                                                    else:  ##Anything greater than 6
                                                                        for word7 in zip(prefix_dict[0][word1[6]], prefix_dict[1][word2[6]],prefix_dict[2][word3[6]], prefix_dict[3][w4[6]], prefix_dict[4][w5[6]], prefix_dict[5][w6[6]]):
                                                                            for w7 in word7:
                                                                                if(w7[0] == word1[6] and w7[1] == word2[6] and w7[2] == word3[6] and w7[3] == w4[6] and w7[4] == w5[6] and w7[5] == w6[6]):
                                                                                    if length == 7:## SEVEN
                                                                                        str = check_letters(input, length, word1, word2, word3,  w4, w5, w6, w7)
                                                                                        if str: print str; return
        except:
            pass ## Dont care about KeyErrors
        
## Check to see if all of the words combined match the input string
def check_letters(input, length, *argv):
    string = ''.join(sorted(''.join(argv)))
    string2 = ''.join(argv)
    compare = ''.join(sorted(input))
    if string == compare:
        chunkstr = "\n"
        chunks = (string2[0+i:length+i] for i in range(0, len(string2), length))
        for chunk in chunks:
            chunkstr += chunk + "\n"
        return chunkstr


## Used when generating the word list - looks for words which contain letters in the input string
def enough_letters(input, *argv):
    string = ''.join(sorted(''.join(argv)))
    compare = sorted(input)
    for char in list(string):
        if char in compare:
            compare.remove(char)
        else:
            return False
    return True
            
            
## Main
def main(length, input):
    pathz = os.getcwd() + "\\words.txt" ## Local path - run the code from the same dir as the words.txt dict
    wordz = wordlist(length, input, sourcefile=pathz) ## Import word dict
    step2, prefix_dict = wordgen(wordz, input, length) ## Use the string input to generate a list of words of a set length
    print "Generating..."
    step4 = generategrid4( step2, length, prefix_dict, input)
 

if __name__ == "__main__": 
	sys.exit(main(int(sys.argv[1]), sys.argv[2]))