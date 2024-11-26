
# malayalamCorefResolve

### Coreference Resolution
It is the task of finding all expressions that refer to the same entity in a text.

We often find use fo coreference resolution for tasks such as 
 - Document Summarisation
 - Question Answering
 - Information Extraction

There are different types of coreference

 - Anaphora
 - Cataphora
 - Split antecedants
 - Corefering noun phares

Most algorithms tend to look for nearest senatance noun individual which matches the restrictions

## How to use it?

### Installation

One of the dependencies hfst pip download works only for 3.7 as of today. Hence, it is recommended to use the application with Python 3.7, untill the build wheels for 3.8 is available for 3.8 via pip. (The easy work around). Myself, I use the application within a virtualnev set to python 3.7.

Once you are on Python 3.7, you can just run

```
pip install -r requirements.txt
```

Now you are ready to go!

####  Use it in your program

```
from corefResolver import  pronounResolutionMal
obj = pronounResolutionMal(text) #Text is the document
```
You can find the result at

```
obj.returnSolutionCandidates()
```

####  Terminal Run

```
python corefResolver.py filename.txt file #If as file
python corefResolver.py rawText #If as text
```
#### Flask app

To use the flask app, 

```
python flaskMain.py
```

## Tools used

1. [Shallow Parser](https://github.com/Devadath/Malayalam-Shallow-Parser)
2. [Mlmorph](https://gitlab.com/smc/mlmorph)
3. [Hobb's algorithm implementation](https://github.com/cmward/hobbs) 
