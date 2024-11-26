import ast
from nltk import Tree
from basicFunctions import readFromFile, writeToFile, get_pos


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

    return mapper
