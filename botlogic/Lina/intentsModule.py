import pandas
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import string
import numpy as np
from re import sub
from os.path import join, dirname


def _getFormattedPlainText(datainput):
    text = ""
    for data in datainput:
        text += str(data) + "\n"
    text = text.lower()
    text = sub('[' + string.punctuation + ']', '', text)
    return text


# return intent type
def getAnswer(inputString, threshold=0.7):
    data = pandas.read_csv(join(dirname(__file__), "intents.csv"))

    inputString = inputString.lower()
    inputString = sub('[' + string.punctuation + ']', '', inputString)

    trainDocs = _getFormattedPlainText(data.Input)
    trainDocsSplitted = trainDocs.split('\n')

    alltext = trainDocs + "\n" + inputString

    globalVector = TfidfVectorizer(lowercase=True, stop_words='english', analyzer='word')
    tfidf_vec = globalVector.fit_transform(alltext.split('\n'))
    pairwise_similarity = (tfidf_vec * tfidf_vec.T).A

    testSim = pairwise_similarity[len(pairwise_similarity) - 1]
    testSim[len(trainDocsSplitted)] = 0

    maxvalue = testSim.max()
    index = np.where(testSim == maxvalue)[0]
    if (maxvalue < threshold):
        return (None, None)
    else:
        _index = np.random.choice(index)
        return (data.Action[_index])
