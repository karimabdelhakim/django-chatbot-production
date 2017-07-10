import pandas
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import string
import numpy as np
import random
from re import sub
from os.path import join, dirname
from standarizeCSV import readAndReWrite


def _getFormattedPlainText(datainput):
    text = ""
    for data in datainput:
        text += str(data) + "\n"
    text = text.lower()
    text = sub('[' + string.punctuation + ']', '', text)
    return text


# return intent type
def getAnswer(inputString, threshold=1):
    try:
        data = pandas.read_csv(join(dirname(__file__), "standarizedIntents.csv"))
    except IOError:
        readAndReWrite()
        data = pandas.read_csv(join(dirname(__file__), "standarizedIntents.csv"))

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
        return ["message"]
    else:
        removeDualFlag = False
        for i in index:
            if (not (" - " in data.Action[i])):
                removeDualFlag = True;
                break;

        if removeDualFlag:
            finalData = []
            for i in index:
                if (not (" - " in data.Action[i])):
                    print data.Action[i]
                    finalData.append(data.Action[i])

            classificationResult = str(random.choice(finalData))
            return classificationResult.split(" - ")

        else:
            _index = np.random.choice(index)
            return str(data.Action[_index]).split(" - ")
