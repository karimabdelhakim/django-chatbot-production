import csv

animation_file = csv.reader(open('Movie_titles/animation.csv', "r"), delimiter=",")

movie_conversations = csv.reader(open('cornell movie-dialogs corpus/movie_conversations delitter.csv', "r"), delimiter=",")
movie_conversations =    [r for r in movie_conversations]

movie_lines = csv.reader(open('cornell movie-dialogs corpus/movie_lines delimted.csv', "r"), delimiter=",")

movie_lines_dict={}      #[r for r in movie_lines]
for r in movie_lines:
   movie_lines_dict[r[0].replace(" ",'')] = r[4]


#conversations ={'question':[] , 'response':[]  ,'Line_id_question':[] , 'Line_id_response':[] , 'movie_id' :[]}
csv_columns = ['question','response','Line_id_question' , 'Line_id_response' , 'movie_id']
conversations=[]
fantasy      = open('fantasy.csv', 'w+')

conversations_opener =   open('animation_conversation.csv', 'wb')
conversations_writer =   csv.DictWriter(conversations_opener, fieldnames=csv_columns)

#animation_conversation       = open('animation_conversation.csv', 'wb')
#csv_animation_conversation   =  csv.writer(animation_conversation   , delimiter=',' ,  lineterminator='\n')


def WriteDictToCSV(dict_data):
    try:
            for data in dict_data:
                conversations_writer.writerow(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))    
    return 

row_count=0
#loop on the file of geners
for row_genre in animation_file:
    movie_id =  row_genre[0]

    #clean
    movie_id = movie_id.replace(" ","")
    conversations=[]

    try:
        # now get conversations ids within this film
        for row_converstion in movie_conversations:
               #clean
               row_converstion[2] = row_converstion[2].replace(" ","")
               row_converstion[2] = row_converstion[2].replace("\'","")

               if  movie_id == row_converstion[2] :

                   #clean columb of utterance id
                   row_converstion[3] = row_converstion[3].replace("[","")
                   row_converstion[3] = row_converstion[3].replace("]","")
                   row_converstion[3] = row_converstion[3].replace("\'","")

                   utternace_id_list  = row_converstion[3].split(",")

                   if len(utternace_id_list) % 2 == 0:
                        note="it is even "
                   else:
                        note="it is odd "
                        utternace_id_list.pop()

                   # now get conversations themselves within this film
                   i=0
                   for L_id in  range(len(utternace_id_list)):

                       if i< L_id:
                           # we need to loop +2
                           sentance_1 = movie_lines_dict[utternace_id_list[i].replace(" ","")]
                           sentance_2 = movie_lines_dict[utternace_id_list[i+1].replace(" ","")]
                           temp={}
                           temp['question']=sentance_1
                           temp['response']=sentance_2
                           temp['Line_id_response']=utternace_id_list[i]
                           temp['Line_id_question']=utternace_id_list[i+1]
                           temp['movie_id']=movie_id
                           conversations.append(temp)

                           i+=2
    except Exception:
         pass

    WriteDictToCSV(conversations)
    print(str(movie_id) + " done el7")
    aaaaa=7541
    
             
                       #with open('animation_conversation.csv', 'wb') as f:  # Just use 'w' mode in 3.x
                       #    writer = csv.writer(f)
                       #    headers = conversations.keys()
                       #    writer.writerow(headers)
                       #    
                       #    for dat in conversations:
                       #        line = []
                       #        for field in headers:
                       #            line.append(dat[field])
                       #        writer.writerow(line)
                           

                           #w = csv.DictWriter(f, conversations.keys())
                          # w.writeheader()
                           #w = csv.DictWriter(f, conversations.keys())
                           #w.writeheader()
                           #w.writerows(conversations.values())

                       #aaaaa=78979  
                      
                      
                      
                      
    #a =98
      













#                       #only first time look for line
#                       if i==0:
#                           j=0
#                           for row_line in movie_lines:
#                               #clean columb of utterance id
#                               row_line[0] = row_line[0].replace(" ","")
#                               row_line[0] = row_line[0].replace("\xef\xbb\xbf","")

#                               line_id     =  row_line[0]
                                                                        
#                               if line_id ==  utternace_id_list[i].replace(" ",""):
#                                  super_line_number  =  j
#                                  sentance_1 = row_line[4]
#                               j+=1
#                           line_number=super_line_number-1
#                           sentance_2 = movie_lines[line_number][4]

#                           conversations['question'].append(sentance_1)
#                           conversations['response'].append(sentance_2)
#                           conversations['Line_id_response'].append(movie_lines[super_line_number-1][0])
#                           conversations['Line_id_question'].append(movie_lines[super_line_number][0])
#                           conversations['movie_id'].append(movie_id)
#                           super_line_number    -=1

#                       #now just use line without searching
#                       else:
#                           line_number=super_line_number-1
#                           sentance_1 = movie_lines[line_number][4]

#                           line_number=line_number-1
#                           sentance_2 = movie_lines[line_number][4]

#                           super_line_number -=2

#                           conversations['question'].append(sentance_1)
#                           conversations['response'].append(sentance_2)
#                           conversations['Line_id_response'].append(movie_lines[super_line_number-1][0])
#                           conversations['Line_id_question'].append(movie_lines[super_line_number][0])
#                           conversations['movie_id'].append(movie_id)
#                       i+=2
#    csv_animation_conversation.writerows(conversations)
#    conversations['question'] =[]        
#    conversations['response'] =[] 
#    conversations['Line_id_question'] =[] 
#    conversations['Line_id_response'] =[] 
#    conversations['movie_id'] =[] 
#    print ( row_converstion[0] + " done")
#    aaaaa=4564654       
#row_count += 1 





