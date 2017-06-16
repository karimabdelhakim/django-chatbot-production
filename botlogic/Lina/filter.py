import pickle
import re
import os
dir = os.path.dirname(__file__)
file_Name = os.path.join(dir,"cursing","curses.pickle")
fileObject = open(file_Name,'r')  
b = pickle.load(fileObject) 

one= b[0]

two = b[1]
pre1_two = b[1][0]
pre2_two = b[1][1]

three = b[2]
pre1_three = b[2][0]
pre2_three = b[2][1]
pre3_three = b[2][2]

four = b[3]
pre1_four = b[3][0]
pre2_four = b[3][1]
pre3_four = b[3][2]
pre4_four = b[3][3]

six = b[4]

MARKS = ",.!?/\\()[]{}<>-_+=@#$%^&*~'\""

def handle_marks(word):
	if word[0] in MARKS and word[-1] in MARKS:
		return handle_marks(word[1:-1])
	elif word[-1] in MARKS:
		return handle_marks(word[:-1])
	elif word[0] in MARKS:
		return handle_marks(word[1:])
	else:
		return word.lower()


def curse_free(sentence):

	line = sentence.split(" ")

	for i in range(len(line)):
		if line[i] == "":
			continue
		word = handle_marks(line[i])

		if word in one:
			return False
		
		elif word in pre1_two:
			word_index = pre1_two.index(word)
			try:
				if line[i+1] == pre2_two[word_index]:
					return False
				else:
					pass
			except:
				pass

		elif word in pre1_three:
			word_index = pre1_two.index(word)
			try:
				if line[i+1] == pre2_three[word_index] and line[i+2] == pre3_three[word_index]:
					return False
				else:
					pass
			except:
				pass

		elif word in pre1_four:
			word_index = pre1_four.index(word)
			try:
				if line[i+1] == pre2_four[word_index] and line[i+2] == pre3_four[word_index] and line[i+3] == pre4_four[word_index]:
					return False
				else:
					pass
			except:
				pass

		elif word in six[0]:
			try:
				if line[i+1] == six[1] and line[i+2] ==six[2] and line[i+3] ==six[3] and line[i+4] ==six[4] and line[i+5] ==six[5]:
					return False
				else:
					pass
			except:
				pass
	
	return True

def curse_no_marks(sentence) :
        for char in MARKS:
             sentence = sentence.replace(char,"")
        
        return  curse_free(sentence)


#USE the curse_free() function which a boolean function that takes a sentence and returns 
# whhether the sentence is curse-free or not, like so:
#while(1):
#	var = curse_no_marks(raw_input("enter your sentance :"))
#	print var


#print curse_free("I love you in a fun way")
#print curse_free("I love you in a fuck way")
#print curse_free("Fucking badass function")
#print curse_free("I think you are a moron, like your brother") #notice the comma in the end of the curse
#print curse_free("I think you are an ass-fuck, like ...")