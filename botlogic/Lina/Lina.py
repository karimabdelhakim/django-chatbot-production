from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import csv
import os

import timeit
import pickle
import random

from stat_parser.parser import Parser, display_tree
# from nltk.chunk import ne_chunk
# from nltk.tag import pos_tag
# from nltk.tokenize import word_tokenize

import nltk
from extract_intents import extract_intents, crop_intents
from intentsModule import getAnswer
from WeatherOrMovies import getResults
from json import loads

# _____Fact Questions Libraries_____
import re
from bs4 import BeautifulSoup
import requests

# _____Curse Fiter_____
import filter

# ______Intent classifier Youssef_____
import pandas
import sklearn
import string

# -----------------------------------$$ Global Variables $$-------------------------------------#
delimeter = "_+^$#*#$^+_"
dir = os.path.dirname(__file__)

# -------------------------Parse and see if it is for internet----------------------------------#

tree_output = []
imp_list_array = {'Noun': []}


def traverse(parent, x):
    try:
        for node in parent:
            if type(node) is nltk.Tree:
                if node.label() == 'ROOT':
                    # "======== Sentence ========="
                    # print "Sentence:", " ".join(node.leaves()) , " +  type " , node.label()
                    a = 6
                else:
                    element_type = node.label()
                    element_value = node.leaves()[0]
                    element_sentence = node.leaves()

                    if str(element_type) == 'NN' or str(element_type) == 'NNS' or str(element_type) == 'NNP' or str(
                            element_type) == 'NNPS':
                        imp_list_array['Noun'].append(str(element_value))

                    # tree_output.append(node)

                    traverse(node, x)
            else:
                # tree_output.append(  node)
                tree_output.append(parent.label())

                # print "Word:", node
                a = 5
    except:
        tree_output.append('NN')


def parse(sentence):
    while len(tree_output) > 0:
        tree_output.pop()

    parser = Parser()
    try:
        tree = parser.parse(sentence)
        print tree
    except:
        return False, ""

    # display_tree(tree)
    print("parse succeeded")

    for i in range(len(tree)):
        traverse(tree[i], 0)

    print("traverse succeeded")
    tree_output_str = ""

    for a in tree_output:
        tree_output_str += " - " + a
    print  tree_output_str
    special_parses = [
        "WRB - JJ - NNS",  # how many Leopards
        "WRB - JJ - JJ",  # how many leopards
        "WRB - JJ - VBP - DT - NN",  # how big are the pyramids
        "WRB - JJ - VBZ - JJ",  # how old is obama
        "WRB - JJ - VBZ - NNP",  # how old is Obama
        "WRB - JJ - NN - VBP - NNP - VBP",  # how much money do Bill have
        "WRB - VBP - DT - NN",  # where are the pyramids
        "WP - VBP - PRP - VB - IN - NN",  # what do you know about egypt

        "WP - VBD - DT - NN",  # who won the champions last week        #when was the tv first invented
        "WP - VBD - NN",  # who worked today

        "WP - VBP - DT - NN",  # what are the pyramids
        "WP - VBZ - DT - NN - IN - NN",  # what is the capital of egypt

        "WDT - NNS",  # which companies are the biggest ,
        "WRB - VBZ - NN",  # where is egypt
        "WP - VBZ - NNP",  # what is Egypt
        "WP - VBZ - JJ",  # what is egypt
        "WRB - VBD - NNP",  # when did Bayern
        "WP - VBZ - NN"  # what is indonesian
    ]

    try:
        # other special parses
        regex = reduce(lambda x, y: x + "|" + y, special_parses)
        print tree_output_str
        pos_tree_output = tree_output_str.index(re.search(regex, tree_output_str).group(0))
        pos_var = len(tree_output_str.replace('-', '').split()) - len(
            tree_output_str[pos_tree_output:].replace('-', '').split())
        print pos_var
        print tree_output_str
        fact_question = ' '.join(sentence.split()[pos_var:])

        print("it is a fact question")
        base_address = "https://api.duckduckgo.com/?q=" + fact_question + "&format=xml"

        super_page = requests.get(base_address)
        print("request succeeded")

        soup_super_page = BeautifulSoup(super_page.content, "xml")
        print("BeautifulSoup succeeded")

        answer = soup_super_page.findAll('Abstract')[0].text
        Image = soup_super_page.findAll('Image')[0].text
        if (answer == ""):
            answer = soup_super_page.findAll('Text')[0].text

        return True, answer, Image
    except Exception as exception:
        print ("error2", exception)
        print (type(exception).__name__)
        print (exception.__class__.__name__)
        return False, ""


        # -----------------------General DataSet   &   Movies Lines----------------#


def talk_to_lina(test_set_sentence, csv_file_path, tfidf_vectorizer_pikle_path, tfidf_matrix_train_pikle_path):
    i = 0
    sentences = []

    # enter your test sentence
    test_set = (test_set_sentence, "")

    # 3ashan yzabt el indexes
    sentences.append(" No you.")
    sentences.append(" No you.")

    try:
        ##--------------to use------------------#
        f = open(tfidf_vectorizer_pikle_path, 'rb')
        tfidf_vectorizer = pickle.load(f)
        f.close()

        f = open(tfidf_matrix_train_pikle_path, 'rb')
        tfidf_matrix_train = pickle.load(f)
        f.close()
        # ----------------------------------------#
    except:
        # ---------------to train------------------#
        start = timeit.default_timer()

        # enter jabberwakky sentence
        with open(csv_file_path, "r") as sentences_file:
            reader = csv.reader(sentences_file, delimiter=',')
            # reader.next()
            # reader.next()
            for row in reader:
                # if i==stop_at_sentence:
                #    break
                sentences.append(row[0])
                i += 1

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
        # tfidf_matrix_test =tfidf_vectorizer.transform(test_set)
        stop = timeit.default_timer()
        print ("training time took was : ")
        print stop - start

        f = open(tfidf_vectorizer_pikle_path, 'wb')
        pickle.dump(tfidf_vectorizer, f)
        f.close()

        f = open(tfidf_matrix_train_pikle_path, 'wb')
        pickle.dump(tfidf_matrix_train, f)
        f.close()
        # -----------------------------------------#

    tfidf_matrix_test = tfidf_vectorizer.transform(test_set)

    cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)

    cosine = np.delete(cosine, 0)
    max = cosine.max()
    response_index = 0
    if (max > 0.7):
        new_max = max - 0.01
        list = np.where(cosine > new_max)
        print ("number of responses with 0.01 from max = " + str(list[0].size))
        response_index = random.choice(list[0])

    else:
        print ("not sure")
        print ("max is = " + str(max))
        response_index = np.where(cosine == max)[0][0] + 2  # no offset at all +3

    j = 0

    with open(csv_file_path, "r") as sentences_file:
        reader = csv.reader(sentences_file, delimiter=',')
        for row in reader:
            j += 1  # we begin with 1 not 0 &    j is initialized by 0
            if j == response_index:

                if delimeter in row[1]:
                    # get newest suggestion
                    answer_row = row[1].split(delimeter)
                    row[1] = answer_row[1]

                else:  # add new suggestion
                    note = "just return old original suggestion"

                return row[1], response_index,
                break


def talk_to_lina_primary(test_set_sentence, csv_file_path, tfidf_vectorizer_pikle_path, tfidf_matrix_train_pikle_path):
    i = 0
    sentences = []

    # enter your test sentence
    test_set = (test_set_sentence, "")

    # 3ashan yzabt el indexes
    sentences.append(" No you.")
    sentences.append(" No you.")

    try:
        ##--------------to use------------------#
        f = open(tfidf_vectorizer_pikle_path, 'rb')
        tfidf_vectorizer = pickle.load(f)
        f.close()

        f = open(tfidf_matrix_train_pikle_path, 'rb')
        tfidf_matrix_train = pickle.load(f)
        f.close()
        # ----------------------------------------#
    except:
        # ---------------to train------------------#
        start = timeit.default_timer()

        # enter jabberwakky sentence
        with open(csv_file_path, "r") as sentences_file:
            reader = csv.reader(sentences_file, delimiter=',')
            # reader.next()
            # reader.next()
            for row in reader:
                # if i==stop_at_sentence:
                #    break
                sentences.append(row[0])
                i += 1

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  # finds the tfidf score with normalization
        # tfidf_matrix_test =tfidf_vectorizer.transform(test_set)
        stop = timeit.default_timer()
        print ("training time took was : ")
        print stop - start

        f = open(tfidf_vectorizer_pikle_path, 'wb')
        pickle.dump(tfidf_vectorizer, f)
        f.close()

        f = open(tfidf_matrix_train_pikle_path, 'wb')
        pickle.dump(tfidf_matrix_train, f)
        f.close()
        # -----------------------------------------#

    tfidf_matrix_test = tfidf_vectorizer.transform(test_set)

    cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)

    cosine = np.delete(cosine, 0)
    max = cosine.max()
    response_index = 0
    if (max > 0.9):
        new_max = max - 0.01
        list = np.where(cosine > new_max)
        print ("number of responses with 0.01 from max = " + str(list[0].size))
        response_index = random.choice(list[0])

    else:
        print ("not sure")
        print ("max is = " + str(max))
        response_index = np.where(cosine == max)[0][0] + 2  # no offset at all +3
        return "null", "null",

    j = 0

    with open(csv_file_path, "r") as sentences_file:
        reader = csv.reader(sentences_file, delimiter=',')
        for row in reader:
            j += 1  # we begin with 1 not 0 &    j is initialized by 0
            if j == response_index:

                if delimeter in row[1]:
                    # get newest suggestion
                    answer_row = row[1].split(delimeter)
                    row[1] = answer_row[1]

                else:  # add new suggestion
                    note = "just return old original suggestion"

                return row[1], response_index,
                break


# -------------------------------------------------------------------------#

# -----------------------Edit Module (RealTime Learn)----------------------#
def edit_real_time(new_sentence, dataset_number, LineID):
    dataset_path = ["Lina_all.csv",
                    "action_conversation.csv",
                    "animation_conversation.csv",
                    "comedy_conversation.csv",
                    "crime_conversation.csv",
                    "drama_conversation.csv",
                    "fantasy_conversation.csv",
                    "film-noir.csv_conversation.csv",
                    "horror_conversation.csv",
                    "romance_conversation.csv",
                    "sci-fi_conversation.csv",
                    "war_conversation.csv"]
    print
    if filter.curse_no_marks(new_sentence):
        try:
            ##relaive path
            if (dataset_number == 0):
                file_path = os.path.join(dir, dataset_path[dataset_number])
            else:
                file_path = get_relative_path(dataset_path[dataset_number])
            ##end relative path
            f = open(file_path, 'r')
            reader = csv.reader(f)
            mylist = list(reader)
            f.close()

            if delimeter in mylist[LineID - 1][1]:
                # discard old suggestion
                answer_row = mylist[LineID - 1][1].split(delimeter)
                mylist[LineID - 1][1] = answer_row[0] + delimeter + new_sentence

            else:  # add new suggestion
                mylist[LineID - 1][1] += delimeter + new_sentence

            my_new_list = open(file_path, 'wb')
            csv_writer = csv.writer(my_new_list)
            csv_writer.writerows(mylist)
            my_new_list.close()
            print ("thanks for your support")
            print
            return "New reply:" + new_sentence
        except:
            return "Server failure couldn't edit reply, please try again"
    else:
        print ("contains swear word")
        return "Couldn't use your message as it contains vulgar/abusive words"


# -------------------------------------------------------------------------#


def callBot(var, option):
    Lina_all_path_primary = get_relative_path("Lina primary.csv")
    tfidf_vectorizer_april_path_primary = get_relative_path("tfidf_vectorizer_april_primary.pickle")
    tfidf_matrix_train_april_path_primary = get_relative_path("tfidf_matrix_train_april_primary.pickle")

    response_primary, line_id_primary = talk_to_lina_primary(var, Lina_all_path_primary,
                                                             tfidf_vectorizer_april_path_primary,
                                                             tfidf_matrix_train_april_path_primary)

    if (response_primary != "null"):
        return "message", (response_primary.capitalize().strip(), option, None)

    result1 = extract_intents(var)
    result2 = getAnswer(crop_intents(var))
    response = ""

    print "anwar:" + str(result1)
    print "youssef:" + str(result2)
    if (result1[0][0] == "message" and result2[0] == "message"):  # not intent
        fact_question = parse(var)  # [False]
        line_id = None
        if (fact_question[0]):
            print "Fact Question"
            # print fact_question[1].encode('utf-8')
            response = fact_question[1].encode('utf-8').split('.')[0] + '.' + fact_question[2]
            print

        else:
            print "action : "
            print ("ENTER CHARACTER:")
            print (
                "general:0   action:1   animation:2   comedy:3   crime:4  drama:5   fantasy:6    filmnoir:7   horror:8  romance:9   scifi:10   war:11")
            # option = int(raw_input("enter option as number: ")   )
            if option == 0:
                Lina_all_path = os.path.join(dir, "Lina_all.csv")
                tfidf_vectorizer_april_path = os.path.join(dir, "tfidf_vectorizer_april.pickle")
                tfidf_matrix_train_april_path = os.path.join(dir, "tfidf_matrix_train_april.pickle")
                response, line_id = talk_to_lina(var, Lina_all_path, tfidf_vectorizer_april_path,
                                                 tfidf_matrix_train_april_path)

            elif option == 1:
                response, line_id = talk_to_lina(var, get_relative_path("action_conversation.csv"),
                                                 get_relative_path('tfidf_vectorizer_action.pickle'),
                                                 get_relative_path('tfidf_matrix_train_action.pickle'))

            elif option == 2:
                response, line_id = talk_to_lina(var, get_relative_path("animation_conversation.csv"),
                                                 get_relative_path('tfidf_vectorizer_animation.pickle'),
                                                 get_relative_path('tfidf_matrix_train_animation.pickle'))

            elif option == 3:
                response, line_id = talk_to_lina(var, get_relative_path("comedy_conversation.csv"),
                                                 get_relative_path('tfidf_vectorizer_comedy.pickle'),
                                                 get_relative_path('tfidf_matrix_train_comedy.pickle'))

            elif option == 4:
                response, line_id = talk_to_lina(var, get_relative_path("crime_conversation.csv"),
                                                 get_relative_path('tfidf_vectorizer_crime.pickle'),
                                                 get_relative_path('tfidf_matrix_train_crime.pickle'))

            elif option == 5:
                response, line_id = talk_to_lina(var, get_relative_path("drama_conversation.csv"),
                                                 get_relative_path('tfidf_vectorizer_drama.pickle'),
                                                 get_relative_path('tfidf_matrix_train_drama.pickle'))

            elif option == 6:
                response, line_id = talk_to_lina(var, get_relative_path("fantasy_conversation.csv"),
                                                 get_relative_path('tfidf_vectorizer_fantasy.pickle'),
                                                 get_relative_path('tfidf_matrix_train_fantasy.pickle'))

            elif option == 7:
                response, line_id = talk_to_lina(var, get_relative_path("film-noir.csv_conversation.csv"),
                                                 get_relative_path('tfidf_vectorizer_film-noir.pickle'),
                                                 get_relative_path('tfidf_matrix_train_film-noir.pickle'))

            elif option == 8:
                response, line_id = talk_to_lina(var, get_relative_path("horror_conversation.csv"),
                                                 get_relative_path('tfidf_vectorizer_horror.pickle'),
                                                 get_relative_path('tfidf_matrix_train_horror.pickle'))

            elif option == 9:
                response, line_id = talk_to_lina(var, get_relative_path("romance_conversation.csv"),
                                                 get_relative_path('tfidf_vectorizer_romance.pickle'),
                                                 get_relative_path('tfidf_matrix_train_romance.pickle'))

            elif option == 10:
                response, line_id = talk_to_lina(var, get_relative_path("sci-fi_conversation.csv"),
                                                 get_relative_path('tfidf_vectorizer_sci-fi.pickle'),
                                                 get_relative_path('tfidf_matrix_train_sci-fi.pickle'))

            elif option == 11:
                response, line_id = talk_to_lina(var, get_relative_path("war_conversation.csv"),
                                                 get_relative_path('tfidf_vectorizer_war.pickle'),
                                                 get_relative_path('tfidf_matrix_train_war.pickle'))

            print

            print ("Lina :  " + response)

        return "message", (response.capitalize().strip(), option, line_id)

    intents_result_no_movies_weather = result1 + map(lambda x: (x,), result2)  # intents
    intents_full_result = list()

    for current_intent in intents_result_no_movies_weather:
        type = current_intent[0]
        if type == "message":
            continue
        elif type == "suggest movie":
            type = random.choice(["top rated", "popular"])
            result = loads(getResults("movie", type))
            resultString = "{0}({1}): {2}\n{3}\n{4},".format(result['Original Title'], result["rating"],
                                                             result["Overview"],
                                                             result["poster"], "Trailer Link")
            intents_full_result.append(('display_message', resultString))
        elif type == "show_movie":
            resultStr = getResults("movie", current_intent[1].split("('")[1].split("')")[0])
            if (resultStr != "No Movie Found"):
                result = loads(resultStr)
                resultString = "{0}({1}):\n{5}\n{2}\n{3}\n{4},".format(result['Original Title'], result["rating"],
                                                                       result["Overview"], result["poster"],
                                                                       result["Trailer Link"],
                                                                       map(lambda genre: genre.encode('ascii',
                                                                                                      'replace'),
                                                                           result['genres']))
                intents_full_result.append(('display_message', resultString))
            else:
                intents_full_result.append(('display_message', resultStr))
        elif type == "show_trailer":
            resultStr = getResults("movie", current_intent[1].split("('")[1].split("')")[0])
            if (resultStr != "No Movie Found"):
                result = loads(resultStr)
                resultString = "{0}({1}):\n{5}\n{2}\n{3}\n{4},".format(result['Original Title'], result["rating"],
                                                                       result["Overview"], result["poster"],
                                                                       result["Trailer Link"],
                                                                       map(lambda genre: genre.encode('ascii',
                                                                                                      'replace'),
                                                                           result['genres']))
                intents_full_result.append(('display_message', resultString))
                intents_full_result.append(('play_trailer', "trailer_link(" + result["Trailer Link"] + ")"))
            else:
                intents_full_result.append(('display_message', resultStr))

        elif type == "recommend_movie":
            result = loads(getResults("movie", "genre:" + current_intent[1].split("('")[1].split("')")[0]))
            resultString = "{0}({1}):\n{5}\n{2}\n{3}\n{4},".format(result['Original Title'], result["rating"],
                                                                   result["Overview"], result["poster"],
                                                                   result["Trailer Link"],
                                                                   map(lambda genre: genre.encode('ascii', 'replace'),
                                                                       result['genres']))
            intents_full_result.append(('display_message', resultString))

        elif type == "show_weather":
            resultStr = getResults("weather", current_intent[1].split("('")[1].split("')")[0])
            if (resultStr != "No Matching City Was Found"):
                result = loads(getResults("weather", type))
                resultString = "{0} with temperature of {1} Celsius and Humidity of {2}".format(
                    result['Weather Condition'],
                    result['Temperature In Celcius'],
                    result['Humidity'])
                intents_full_result.append(('display_message', resultString))
            else:
                intents_full_result.append(('display_message', resultStr))

        else:
            intents_full_result.append(current_intent)
    return 'intent', intents_full_result


def get_relative_path(filename):
    conversations_dir = os.path.join(dir, "Conversations")
    relative_path = os.path.join(conversations_dir, filename)
    return relative_path
