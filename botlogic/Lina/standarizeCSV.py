import pandas
import numpy as np
import string
from re import sub
from os.path import join, dirname


def _getFormattedPlainText(datainput):
    text = ""
    for data in datainput:
        text += str(data) + "\n"
    text = text.lower()
    text = sub('[' + string.punctuation.replace("_", "") + ']', '', text)
    return text


def _getPermutedText(iterable, numberOfPerm):
    pool = tuple(iterable)
    n = len(pool)
    if numberOfPerm > n:
        return
    indices = list(range(numberOfPerm))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(numberOfPerm)):
            if indices[i] != i + n - numberOfPerm:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, numberOfPerm):
            indices[j] = indices[j - 1] + 1
        yield tuple(pool[i] for i in indices)


def _formatInput(permutedText, mainText, isInput):
    concatStr = " - "
    if isInput:
        concatStr = " and "
    formatedPermutedtext = []
    for element in permutedText:
        formatedPermutedtext.append(element[0] + concatStr + element[1])

    return formatedPermutedtext + mainText


def _removeReplicas(trainData_x, trainData_y):
    newTrainData_Y = []
    newTrainData_X = []
    for i, j in zip(trainData_x, trainData_y):
        classes = j.split(' - ')
        if (len(classes) > 1):
            if (classes[0] != classes[1]):
                newTrainData_X.append(i)
                newTrainData_Y.append(j)

        else:
            newTrainData_X.append(i)
            newTrainData_Y.append(j)

    return (newTrainData_X, newTrainData_Y)


def readAndReWrite():
    data = pandas.read_csv(join(dirname(__file__), "intents.csv"))
    print type(data)

    trainDocs_x = _getFormattedPlainText(data.Input)
    trainDocs_x = trainDocs_x.split('\n')

    trainDocs_y = _getFormattedPlainText(data.Action)
    trainDocs_y = trainDocs_y.split('\n')

    if ('' in trainDocs_y):
        trainDocs_y.remove('')
    if ('' in trainDocs_x):
        trainDocs_x.remove('')

    permutedTraindDocs_x = list(_getPermutedText(trainDocs_x, 2))
    permutedTraindDocs_y = list(_getPermutedText(trainDocs_y, 2))

    main_items_x = list(data.Input)
    main_items_y = list(data.Action)

    main_items_x = _getFormattedPlainText(main_items_x)
    main_items_x = main_items_x.split('\n')
    main_items_y = _getFormattedPlainText(main_items_y)
    main_items_y = main_items_y.split('\n')

    trainData_x = _formatInput(permutedTraindDocs_x, main_items_x, True)
    trainData_y = _formatInput(permutedTraindDocs_y, main_items_y, False)

    (trainData_x, trainData_y) = _removeReplicas(trainData_x, trainData_y)

    dataToWrite = np.array([trainData_x, trainData_y]).T

    x = pandas.DataFrame(dataToWrite, columns=["Input", "Action"])
    x.to_csv(path_or_buf=join(dirname(__file__), "standarizedIntents.csv"), index=False)
