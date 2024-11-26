from nltk import Tree


def writeToFile(text, targetFile, mode='w'):
    '''
    When you write to file, half spaces are
    written as it's unicode representation. 
    Printing to file is a better alternative
    '''
    if mode == 'a':
        # Means I am writing to log file
        print(text)
    with open(targetFile, mode) as targetFile:
        print(text, file=targetFile)


def readFromFile(targetFile):
    '''
    Read from target file
    '''
    with open(targetFile, 'r') as targetFile:
        text = targetFile.read()
    return text


def get_pos(tree, node):
    """ Given a tree and a node, return the tree position
    of the node. 
    """

    for pos in tree.treepositions():
        if tree[pos] == node:
            return pos


def returnPronouns(tokenisedSentances, wordsList, parseSents, returnText=False):
    #parseSents = ast.literal_eval(readFromFile('temp/parseString.txt'))
    #tokenisedSentances = list(filter(None,readFromFile('temp/tokens.txt').split('\n')))
    #wordsList = [sentance.split(' ') for sentance in tokenisedSentances]
    mapper = {}
    trees = [Tree.fromstring(s) for s in parseSents]
    for treeno in range(len(trees)):
        minimap = []
        for sub_tree in trees[treeno].subtrees():
            if sub_tree.label() == 'PRP' or sub_tree.label() == 'PRN':
                pronoun = sub_tree.leaves()[0]
                minimap.append(pronoun)
        for item in list(set(minimap)):
            mapper[treeno] = list(
                set([wordsList[treeno].index(pronoun) for pronoun in minimap]))

    writeToFile(mapper, 'temp/pronouns.txt')
    writeToFile('Pronouns Resolved', 'temp/logfile.txt', 'a')

    return mapper
