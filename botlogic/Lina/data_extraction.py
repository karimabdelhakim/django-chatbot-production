from stat_parser import Parser, display_tree
import nltk
import re
#import nltk.classify.util
#import pickle

#-------------------------Parse and traverse----------------------------------#

#tree_output = []
imp_list_array={ 'Noun': [] }

def travers_global(parent , x ,tree_output):
    
    traverse(  parent , x , tree_output )
    return  tree_output

def traverse(parent , x , tree_output):
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == 'ROOT':
                # "======== Sentence ========="
                #print "Sentence:", " ".join(node.leaves()) , " +  type " , node.label()
                a=6
            else:
                 element_type  = node.label()
                 element_value = node.leaves()[0]
                 element_sentence = node.leaves()
                 
                 if str(element_type) =='NN'  or str(element_type) =='NNS' or str(element_type) =='NNP' or str(element_type) =='NNPS':
                    imp_list_array['Noun'].append(str(element_value))

                 #tree_output.append(node)

                 traverse(node,x ,tree_output )
        else:
             #tree_output.append(  node)
             tree_output.append(parent.label())

             #print "Word:", node
             a=5
    

def parse(sentenace):

    parser = Parser()
    try:
        tree = parser.parse(sentenace) 
    except:
         return False,""

    #print("parse succeded")
    tree_output_local =[]
    for i in range(len(tree)):
        travers_global(tree[i] , 0 ,tree_output_local )   

    #print("traverse succeded")  
    tree_output_str=""

    for a in tree_output_local  :
         tree_output_str +=" - " + a

    return tree_output_str

#-------------------------Data Extraction----------------------------------#

def regex_my_best_book_is(sentenace , tree_output_str):
    special_parses=[
   "PRP - JJS - NN - VBZ - JJ"  , 
   "PRP - JJS - NN - VBZ - NNP"  ,      
   "PRP - JJS - NN - VBD - JJ"  ,          
   "PRP - JJS - NN - VBD - VBG - DT - NN"   ,
   "PRP - JJS - NN - VBZ - NNP - NNP"
   ]
    tree_output_str = tree_output_str.replace("$" , "")

    regex = reduce(lambda x, y: x + "|" + y, special_parses)
    pos_tree_output = tree_output_str.index(re.search(regex, tree_output_str).group(0))

    pos_var = len(tree_output_str.replace('-', '').split()) - len(
                  tree_output_str[pos_tree_output:].replace('-', '').split())

    fact = ' '.join(sentenace.split()[pos_var:])

    fact_parts =  fact.split(" ")

    who =   fact_parts[0]
    adjective = fact_parts[1]
    noun = fact_parts[2]
    interest = fact_parts[4:]
  
    aap=456
    reply = "The " +   adjective  + " " + noun + " you say ? "
    return reply
    #return who ,adjective ,noun ,interest

def regex_my_name_is(sentenace , tree_output_str):
    special_parses=[
   "PRP - NN - VBZ - NNP"  ,    
   "PRP - NN - VBZ - CD - NNS" 
   ]
    tree_output_str = tree_output_str.replace("$" , "")

    regex = reduce(lambda x, y: x + "|" + y, special_parses)
    pos_tree_output = tree_output_str.index(re.search(regex, tree_output_str).group(0))

    pos_var = len(tree_output_str.replace('-', '').split()) - len(
                  tree_output_str[pos_tree_output:].replace('-', '').split())

    fact = ' '.join(sentenace.split()[pos_var:])

    fact_parts =  fact.split(" ")

    who =   fact_parts[0]
    noun = fact_parts[1]
    interest = fact_parts[3:len(fact_parts)]

    reply = ""

    try:
            reply = interest[0] +" is your name you say ? , what a beautiful "   + noun + " , "
    except aaa:
         pass
    return reply  # return who  ,noun ,interest ,"what"

def regex_i_live_in(sentenace , tree_output_str):
    special_parses=[   
    "VB - IN - NNP"      ,
     ]

    special_parses_with_a=[   
    "VB - IN - NNP"      ,
    "VB - IN - DT - NN"        ,
     ]
    try:
        tree_output_str = tree_output_str.replace("$" , "")

        regex = reduce(lambda x, y: x + "|" + y, special_parses)
        pos_tree_output = tree_output_str.index(re.search(regex, tree_output_str).group(0))

        pos_var = len(tree_output_str.replace('-', '').split()) - len(
                        tree_output_str[pos_tree_output:].replace('-', '').split())

        fact = ' '.join(sentenace.split()[pos_var:])

        fact_parts =  fact.split(" ")

        who =   fact_parts[0]
        verb =  fact_parts[1]
        question_type =""

        reply =""



        interest = fact_parts[2:len(fact_parts)]

        if fact_parts[1] == "in" or fact_parts[1] == "at"  :
            question_type ="where"
            reply = interest[0] +" you say ? "+ "  what a beautiful place ! "

    except :
        tree_output_str = tree_output_str.replace("$" , "")

        regex = reduce(lambda x, y: x + "|" + y, special_parses_with_a)
        pos_tree_output = tree_output_str.index(re.search(regex, tree_output_str).group(0))

        pos_var = len(tree_output_str.replace('-', '').split()) - len(
                        tree_output_str[pos_tree_output:].replace('-', '').split())

        fact = ' '.join(sentenace.split()[pos_var:])

        fact_parts =  fact.split(" ")

        who =   fact_parts[0]
        verb =  fact_parts[1]
        question_type =""

        reply =""

        interest = fact_parts[3:len(fact_parts)]

        reply = interest[0] + " you say ?  interesting ! tell me more about how you became a " + interest[0]

       #else:
       # question_type ="what"


    return reply  #return who  ,verb,interest   ,question_type

def regex_i_am_years_old(sentenace , tree_output_str):
    special_parses=[   
    "JJ - JJ - CD - NNS - JJ"  ,
    "PRP - VB - CD - NNS - JJ"
     ]

    tree_output_str = tree_output_str.replace("$" , "")

    regex = reduce(lambda x, y: x + "|" + y, special_parses)
    pos_tree_output = tree_output_str.index(re.search(regex, tree_output_str).group(0))

    pos_var = len(tree_output_str.replace('-', '').split()) - len(
                  tree_output_str[pos_tree_output:].replace('-', '').split())

    fact = ' '.join(sentenace.split()[pos_var:])

    fact_parts =  fact.split(" ")

    years_old =   fact_parts[2]

    reply= ""
    if  int(years_old)  < 30  :
         reply =  years_old +" is your age ? "  +" still young !  "

    if  int(years_old)  > 30 :
         reply =  years_old  +" is your age ?  never too old  ! "
     
    return reply #return years_old

def regex_i_am_noun(sentenace , tree_output_str):
    special_parses=[   
    "PRP - VB - NNP"
     ]

    tree_output_str = tree_output_str.replace("$" , "")

    regex = reduce(lambda x, y: x + "|" + y, special_parses)
    pos_tree_output = tree_output_str.index(re.search(regex, tree_output_str).group(0))

    pos_var = len(tree_output_str.replace('-', '').split()) - len(
                  tree_output_str[pos_tree_output:].replace('-', '').split())

    fact = ' '.join(sentenace.split()[pos_var:])

    fact_parts =  fact.split(" ")

    interst =   fact_parts[2]

    reply = interst + " you say ? interesting ! "
    return reply #return interst

def regex_stay(sentenace , tree_output_str):

    #for 1 week/s , for 1 day/s
    number = ""
    number_type = ""
    try:
        special_parses=[   
        "IN - CD - NN" ,# for 1 week/s , for 1 day/s
         ]

        tree_output_str = tree_output_str.replace("$" , "")

        regex = reduce(lambda x, y: x + "|" + y, special_parses)
        pos_tree_output = tree_output_str.index(re.search(regex, tree_output_str).group(0))

        pos_var = len(tree_output_str.replace('-', '').split()) - len(
                      tree_output_str[pos_tree_output:].replace('-', '').split())

        fact = ' '.join(sentenace.split()[pos_var:])

        fact_parts =  fact.split(" ")

        number =   fact_parts[1]
        type   =   fact_parts[2]

        reply = " so you want to stay for " + number + " " + type + " am I correct ? "
    except :
        pass
    
    #in early June
    type_month = ""
    month = ""
    try:
        special_parses=[   
        "IN - JJ - NNP" ,# in early June
         ]

        tree_output_str = tree_output_str.replace("$" , "")

        regex = reduce(lambda x, y: x + "|" + y, special_parses)
        pos_tree_output = tree_output_str.index(re.search(regex, tree_output_str).group(0))

        pos_var = len(tree_output_str.replace('-', '').split()) - len(
                      tree_output_str[pos_tree_output:].replace('-', '').split())

        fact = ' '.join(sentenace.split()[pos_var:])

        fact_parts =  fact.split(" ")

        type_month =   fact_parts[1]
        month   =   fact_parts[2]

        reply += type_month + " "  + month + " is a truly perfect period  , " 
    #in  June
    except:
        try:
            special_parses=[   
            "IN - NNP" ,# in June
             ]

            tree_output_str = tree_output_str.replace("$" , "")

            regex = reduce(lambda x, y: x + "|" + y, special_parses)
            pos_tree_output = tree_output_str.index(re.search(regex, tree_output_str).group(0))

            pos_var = len(tree_output_str.replace('-', '').split()) - len(
                          tree_output_str[pos_tree_output:].replace('-', '').split())

            fact = ' '.join(sentenace.split()[pos_var:])

            fact_parts =  fact.split(" ")

            month =   fact_parts[1]

            reply += month + " is a truly perfect month , " 

        except :
            pass
    
    
    months_early = ["January"   ,
                    "February"  ,
                    "March"     ,
                    "April"     ,
                    "May"       ,
                    "June"      ]
    months_late = ["July"      ,
                   "August"    ,
                   "September" ,
                   "October"   ,
                   "November"  ,
                   "December"  ,  ]

    reply += " so we have a package in " 
    if type_month != "":
            if  type_month == "early" :
                 reply += "2nd to 8th  of"
            elif  type_month == "late" :
                 reply += "20th to 28th  of"

    if month in  months_late:
        reply +=  month + " , in Cairo, including a Nile cruise and a Pyramids visit. Would you like to know more?  "
    elif month in  months_early:
       reply +=  month + " , in Alex, including a visit to QayedBay . Would you like to know more?  "
                                                  
    return reply                         

#----------------------------------NLTK sentiment Classifier-------------------------------------#

#def feelings(sentence):
#    #to use saved classifier
#    f = open('my_classifier.pickle', 'rb')
#    classifier = pickle.load(f)
#    f.close()

#    #test_sentence = "This is an bad game"
#    result=classifier.classify(word_feats(sentence))
#    prob_result=classifier.prob_classify(word_feats(sentence))

#    return result , prob_result

#def word_feats(words):
#    return dict([(word, True) for word in words])
#------------------------------------------------------------------------------------------------#
test_sent =[
"my best book is SpeedLink                ",
"my worst nightmare was dark		      "     ,
"my best experiance was riding a bike	  " 	,
"my best book is Harry Potter                ",


"my name is Amr					          " ,
"my height is 20 meter				      " ,

"i live in Egypt					      "     ,
"i work at AinShams					      " ,
"i work as Developer					  "     ,
"i play in a team					      " ,

"i like eating in a cafe			      "     ,
"i hate playing with them		          " ,

"i like eating Pizza			          "     ,
"i hate playing  Tennis                   "      ,

"i am 23 years old"                               


]

#sentence = "my best book is Harry potter what's yours ?"
#sentence = "my height is 20 meters"
#sentence_global = "my name is Amr , I am Egyptian , my best book is Harry Potter , i work as a developer , I live in Egypt"
#sentence_global = "would you please regester me for 12 days in July" 

def data_extraction (sentence_global ) :
    reply_global_string =""

    tree_output_str=""
    #tree_output=[]

    sentence_array=[]
    who_array             = []
    adjective_array       = []
    noun_array            = []
    interest_array        = []
    question_type_array   = []
    verb_array            = []
    years_old_array       = []

    if "," in sentence_global :
       sentence_array =  sentence_global.split(",")
    else  :
       sentence_array.append(sentence_global)

    for  sentence  in    sentence_array :
        tree_output_str = ""
        #tree_output =[]
        tree_output_str = parse(sentence)

        try:
            #(who ,adjective ,noun ,interest , question_type)   
            reply_global_string +=  regex_my_best_book_is(sentence , tree_output_str)

        except :
            pass

        try:
            #(who  ,noun ,interest , question_type)   =  regex_my_name_is(sentence , tree_output_str)
            reply_global_string +=     regex_my_name_is(sentence , tree_output_str)
        
        except :
            pass

        try:
            #(who  ,verb ,interest , question_type)   =  regex_i_live_in(sentence , tree_output_str)
            reply_global_string +=     regex_i_live_in(sentence , tree_output_str)
        except :
            pass

        try:
            #(years_old)   =  regex_i_am_years_old(sentence , tree_output_str)
            reply_global_string +=     regex_i_am_years_old(sentence , tree_output_str)
        except :
            pass

        try:
            #(noun)   =  regex_i_am_noun(sentence , tree_output_str)
            reply_global_string +=     regex_i_am_noun(sentence , tree_output_str)
        except :
            pass


        try:
            reply_global_string   +=  regex_stay(sentence , tree_output_str)
        except :
            pass
    
        aaaa=465
        #parse_sol=[]
        #for a in test_sent:		  
        #    parse_sol.append(parse(a))
        #    tree_output = []


    aaaaaa=46546   #r=798
    return  reply_global_string



#(result , prob_result) =feelings("this is a very bad game ")
#print result
#print prob_result
