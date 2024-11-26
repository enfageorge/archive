

# 📄 Extractive Summarisation using Glove Embeddings and Text Rank.

### Problem Statement:

Identify k most imporatant ie most informational and representative sentences in a document to produce an extractive Summarisation.

### DataSet used

The dataset used in this project is the buissness section of [BBC News Summary Dataset](https://www.kaggle.com/pariza/bbc-news-summary) . It has been modified a bit to fit the solution as outlined in the notebook.

### 🤔 Why load the spacy model instead of using the nltk tokeniser for tokenisation? 

Nltk's default tokenisation - `sent_tokenize()` depends on `PunktSentenceTokenizer` which is an implementation of [Unsupervised Multilingual Sentence Boundary Detection (Kiss and Strunk (2005)](http://old.linguistics.rub.de/~strunk/ks2005FINAL.pdf).

For this given text , from the dataset, (trimmed for brevity)

> "Yukos will return to a US court on Wednesday to seek sanctions against Baikal Finance Group, the little-known firm which has bought its main asset.Yukos has said it will sue Baikal and others involved in the sale of Yuganskneftegas for $20bn in damages.Yukos' US lawyers will attempt to have Baikal assets frozen after the Russian government ignored a US court order last week blocking the sale.Yukos' US lawyers claim the auction was illegal because the firm had filed for bankruptcy and therefore its assets were now under the protection of US bankruptcy law which has worldwide jurisdiction.

Here is how nltk tokenize behaves.

    from nltk.tokenize import sent_tokenize
    
    for sentence in sent_tokenize(summary):
	    print(sentence,"\n")

>Yukos will return to a US court on Wednesday to seek sanctions against Baikal Finance Group, the little-known firm which has bought its main asset.Yukos has said it will sue Baikal and others involved in the sale of Yuganskneftegas for $20bn in damages.Yukos' US lawyers will attempt to have Baikal assets frozen after the Russian government ignored a US court order last week blocking the sale.Yukos' US lawyers claim the auction was illegal because the firm had filed for bankruptcy and therefore its assets were now under the protection of US bankruptcy law which has worldwide jurisdiction.

It return untokenised. But if I were to modify it a little bit, and add spaces after the end of sentence fullstops, this is the result.

    for sentence in sent_tokenize(summary):
	    print(sentence,"\n")

    Yukos will return to a US court on Wednesday to seek sanctions against Baikal Finance Group, the little-known firm which has bought its main asset.Yukos has said it will sue Baikal and others involved in the sale of Yuganskneftegas for $20bn in damages. 

    Yukos' US lawyers will attempt to have Baikal assets frozen after the Russian government ignored a US court order last week blocking the sale. 

    Yukos' US lawyers claim the auction was illegal because the firm had filed for bankruptcy and therefore its assets were now under the protection of US bankruptcy law which has worldwide jurisdiction.

It appears that the nltk default Tokeniser behaves well only over well formed sentences. The spacy tokeniser is able to capture sentence boundaries even if the sentences aren't as well formed.

### ☑️ Things I would like to add to it

 - [ ] Proper Evalution of Summaries returned via the method.
 - [ ]  A blog to go with this, explaining while demonstrating the tools/methods used here, ie
	 - [ ] Glove Embeddings
	 - [ ] Cosine Similarity
	 - [ ] TextRank Algorithm

> Written with [StackEdit](https://stackedit.io/).

