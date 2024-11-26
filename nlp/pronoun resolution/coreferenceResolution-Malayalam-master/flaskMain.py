from flask import session
import ast
from corefResolver import pronounResolutionMal
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/')
def contact():
    return render_template('index.html')


@app.route("/identifypronouns", methods=['POST'])
def identifypronouns():

    session.pop('text', None)
    text = request.form["text"]

    textFile = request.files['file']
    if text == "":
        text = textFile.readline().decode('UTF-8')
    session['text'] = text

    obj = pronounResolutionMal(text)
    pronouns = obj.returnPronounText()
    session.pop('pronouns', None)
    session['pronouns'] = str(pronouns) #Else TypeError: keys must be str, int, float, bool or None, not tuple


    solutions = obj.solutions
    session.pop('solutions', None)
    session['solutions'] = str(solutions) #Else TypeError: keys must be str, int, float, bool or None, not tuple

    wordsList = obj.wordsList
    session.pop('wordsList', None)
    session['wordsList'] = str(wordsList)

    parsableString = obj.parsableString
    session.pop('parsableString', None)
    session['parsableString'] = str(parsableString)

    return render_template('identifyMentions.html', text=text, data=pronouns)


@app.route("/result", methods=['POST'])
def result():
    text = session['text']

    pronounToResolveTuple = ast.literal_eval(request.form["pronoun"])
    session.pop('pronounToResolveTuple', None)
    session['pronounToResolveTuple'] = str(pronounToResolveTuple)

    solutions = ast.literal_eval(session['solutions'])
    wordsList = ast.literal_eval(session['wordsList'])
    mention = solutions[pronounToResolveTuple[0]][pronounToResolveTuple[1]][0]
    pronounToResolve = wordsList[pronounToResolveTuple[0]][pronounToResolveTuple[1]]
    return render_template('result.html', text=text, pronoun=pronounToResolve, mention=mention)

@app.route("/otherOptions", methods=['POST'])
def otherOptions():
    text = session['text']

    pronounToResolveTuple = ast.literal_eval(session['pronounToResolveTuple'])
    
    solutions = ast.literal_eval(session['solutions'])
    wordsList = ast.literal_eval(session['wordsList'])
    mention = solutions[pronounToResolveTuple[0]][pronounToResolveTuple[1]]
    pronounToResolve = wordsList[pronounToResolveTuple[0]][pronounToResolveTuple[1]]
    return render_template('otherOptions.html', text=text, pronoun=pronounToResolve, mention=mention)


@app.route("/debug", methods=['POST'])
def debug():
    text = session['text']

    pronounToResolveTuple = ast.literal_eval(session['pronounToResolveTuple']) 
    solutions = ast.literal_eval(session['solutions'])
    wordsList = ast.literal_eval(session['wordsList'])
    mention = solutions[pronounToResolveTuple[0]][pronounToResolveTuple[1]][0]
    pronounToResolve = wordsList[pronounToResolveTuple[0]][pronounToResolveTuple[1]]
    parseString = session['parsableString']
    return render_template('debug.html', text=text, pronoun=pronounToResolve, mention=mention, parseTree=parseString)

if __name__ == '__main__':
    app.run(debug=True)
