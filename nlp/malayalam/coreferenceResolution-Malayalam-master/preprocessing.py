import os
from mlmorph import Analyser
from polyglot.text import Text
from basicFunctions import readFromFile, writeToFile


analyser = Analyser()


def tokeniseSentances(text):
    """
    Split the text into sentances
    """
    tokenised = Text(text)
    tokenisedSentances = tokenised.sentences
    tokenisedSentances = [str(sentance) for sentance in tokenisedSentances]
    text = '\n'.join(tokenisedSentances)
    writeToFile(text, 'temp/tokens.txt')
    writeToFile('Document Tokenised', 'temp/logfile.txt', 'a')
    return tokenisedSentances


def chunking(text):
    os.chdir('parsing')
    os.system('sh parserForProgram.sh')
    os.chdir('../')
    chunkString = readFromFile('temp/chunkedText')
    writeToFile('Document Chunked', 'temp/logfile.txt', 'a')
    return chunkString


def chunkStringToList(chunkString):
    singleSentanceTokenised = []
    sentancesTokenised = []
    for token in list(filter(None, chunkString.split('\n'))):
        tokenList = list(filter(None, token.split('\t')))
        singleSentanceTokenised.append(tokenList)
        if tokenList[0] in ['.', '?', '!']:
            sentancesTokenised.append(singleSentanceTokenised)
            singleSentanceTokenised = []
    return sentancesTokenised


def returnPOSTaggedDoc(text):
    """
    Returns the pos tagged document.For this,
    the tokenised sentances should be saved at
    temp/tokens.txt
    """
    chunkString = chunking(text)
    chunksList = chunkStringToList(chunkString)
    return chunksList


def nounPhraseExtraction(chunksList):
    """
    Non-Noun Phrases will not contain 
    the possible candidate. Hence filtering
    them out"""
    OnlyNounPhrases = []
    for sentancechunked in chunksList:
        NounPhrases = [item for item in sentancechunked if 'NP' in item[2]]
        OnlyNounPhrases.append(NounPhrases)
    return OnlyNounPhrases


def returnMorphanalysis(word):
    try:
        analysis = analyser.analyse(word)[0][0]
    except IndexError:  # What is happening here?
        analysis = '<UNKNOWN>'
    tags = list(filter(None, analysis.upper().replace(
        '<', ' ').replace('>', ' ').split(' ')))[1:]
    tagsonly = [item for item in tags if item.isupper()]
    return tagsonly


def integrateMorph(chunksList):
    """
    Intergrate the morphological analysis
    into the parse String
    """
    morphList = chunksList
    for sentance in chunksList:
        for word in sentance:
            morph = returnMorphanalysis(word[0])
            for mph in morph[::-1]:
                morphList[morphList.index(sentance)][
                    sentance.index(word)].insert(1, mph)
        writeToFile(morphList, 'temp/morph')
    return morphList


def listToParsableString(chunksList):
    # There are duplicate tags. For eg: N Remove that.
    treesentances = []
    for sentance in chunksList:
        treetext = '( S  '
        layerstoclose = 1
        for token in sentance:
            postags = token[-2].split('__')
            if token[-1].find('B-') != -1:
                if layerstoclose > 1:
                    treetext = treetext + ' ) ' * (layerstoclose - 1)
                    layerstoclose = 1
                treetext = treetext + ' ( ' + 'CHUNK '
                layerstoclose += 1

            # Now add the POS tags
            tags = postags + token[1:len(token) - 2]

            for postag in tags:
                treetext = treetext + ' ( ' + postag
                layerstoclose += 1
            treetext = treetext + ' ' + token[0] + ' ) ' * 2

            layerstoclose -= 2

        treetext = treetext + ' ) ' * layerstoclose

        treesentances.append(treetext)
    return treesentances


def returnParseString(chunksList):
    nounPhraseChunk = nounPhraseExtraction(chunksList)
    morphintList = integrateMorph(nounPhraseChunk)
    parseString = listToParsableString(morphintList)
    writeToFile(parseString, 'temp/parseString.txt')
    writeToFile('Morphological Analysis performed', 'temp/logfile.txt', 'a')
    return parseString
