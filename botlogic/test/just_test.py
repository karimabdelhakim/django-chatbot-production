from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import csv

import timeit

def talk_to_lina(test_set_sentance):
    i=0
    sentences=[]

    #enter your test sentance 
    test_set = (test_set_sentance,"")


    #malaksh da3awa beeh
    #sentences.append(" No you.")

    #tell which sentance to stop training at
    #stop_at_sentence =20

               #enter jabberwakky sentance
    #with open("Lina.csv", "r") as sentences_file:
    #    reader = csv.reader(sentences_file, delimiter=',')
    #    #reader.next()
    #    #reader.next()
    #    for row in reader:
    #        #if i==stop_at_sentence:
    #        #    break
    #        sentences.append(row[0])
    #        i+=1


    #start = timeit.default_timer()

    #tfidf_vectorizer = TfidfVectorizer()
    #tfidf_matrix_train = tfidf_vectorizer.fit_transform(sentences)  #finds the tfidf score with normalization
    ##tfidf_matrix_test =tfidf_vectorizer.transform(test_set)
    #stop = timeit.default_timer()
    #print ("training time took was : ")
    #print stop - start 


    import pickle

    #---------------to save------------------
    #f = open('tfidf_vectorizer_all.pickle', 'wb')
    #pickle.dump(tfidf_vectorizer, f)
    #f.close()

    #f = open('tfidf_matrix_train_all.pickle', 'wb')
    #pickle.dump(tfidf_matrix_train, f)
    #f.close()

    ##--------------to use------------------
    f = open('tfidf_vectorizer_all.pickle', 'rb')
    tfidf_vectorizer = pickle.load(f)
    f.close()

    f = open('tfidf_matrix_train_all.pickle', 'rb')
    tfidf_matrix_train = pickle.load(f)
    f.close()
    tfidf_matrix_test =tfidf_vectorizer.transform(test_set)

    cosine = cosine_similarity(tfidf_matrix_test, tfidf_matrix_train)  


    cosine = np.delete(cosine,0)
    response_index = np.where(cosine == cosine.max())[0][0] +2# no offset at all +3

    j=0
    with open("Lina.csv", "r") as sentences_file:
       reader = csv.reader(sentences_file, delimiter=',')
       for row in reader:
           j += 1 # we begin with 1 not 0 &    j is initialized by 0
           if j == response_index: 
               return row[1]
               break



var = raw_input("Talk to Lina: ")
print "Lina : " +  talk_to_lina(var)