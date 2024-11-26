import sys
import basicFunctions as bf
import preprocessing as prep
import pronounResolver as resolve


class pronounResolutionMal():

    def __init__(self, text, returnAllCandidates=True):
        super(pronounResolutionMal, self).__init__()
        self.text = self.inputText(text)
        self.returnAllCandidates = returnAllCandidates
        self.tokensiedSentances = prep.tokeniseSentances(self.text)
        self.wordsList = [sentance.split(' ')
                          for sentance in self.tokensiedSentances]
        self.posTagged = prep.returnPOSTaggedDoc(self.text)
        self.parsableString = prep.returnParseString(self.posTagged)
        self.pronouns = bf.returnPronouns(
            self.tokensiedSentances, self.wordsList, self.parsableString)
        self.solutions = resolve.resolvePronouns(
            self.tokensiedSentances, self.wordsList, self.parsableString, self.pronouns, self.returnAllCandidates)
        self.pronouns = self.updatePronouns()

    def inputText(self, text):
        """
        Writes the inputText to file
        """
        bf.writeToFile(text, 'temp/inputText.txt')
        bf.writeToFile('Text accepted', 'temp/logfile.txt')
        return text

    def updatePronouns(self):
        updatePronounDict = {}
        for sentanceno, pronoundict in self.solutions.items():
            pronouns = pronoundict.keys()
            updatePronounDict[sentanceno] = pronouns
        return updatePronounDict

    def returnPronounText(self):
        options = {}
        for sentanceno, pronounsno in self.pronouns.items():
            for pronoun in pronounsno:
                options[(sentanceno, pronoun)] = self.wordsList[sentanceno][
                    pronoun] + ' in the sentance ' + self.tokensiedSentances[sentanceno]
        return options

    def returnSolutionCandidates(self):
        candidates = []
        for sentanceno, pronounsnumbers in self.solutions.items():
            for pronounsno in pronounsnumbers.keys():
                if self.solutions[sentanceno][pronounsno] != []:
                    option = 'In the sentance ' + self.tokensiedSentances[sentanceno] + ' the pronoun ' + self.wordsList[
                        sentanceno][pronounsno] + ' refers to ' + str(self.solutions[sentanceno][pronounsno])
                    candidates.append(option)
        return candidates


def main(argv):
    if len(sys.argv) == 3 and sys.argv[2] == 'file':
        with open(fname) as f:
            text = f.readlines()
    elif len(sys.argv) == 2:
        text = sys.argv[1]
        print(text)

    obj = pronounResolutionMal(text)  # Text is the document
    for item in obj.returnSolutionCandidates():
        print(item)


if __name__ == "__main__":
    main(sys.argv)
