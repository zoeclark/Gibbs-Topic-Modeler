#!/bin/bash
import sys
import math
import decimal
from collections import defaultdict
import random
from itertools import islice

def initilize(corpus, topicsList):
    """
    takes in a corpus and empty topic list. Randomly assigns all words in the   
    corpus to a topic. Tells each document about each topic that has been assigned to it. Tells all topics each word that has been 
	assigned to it. Returns a list of documents with topic assignments, and a list of topics with word assignments.
    """
    docList = []
    docCount = 1
    probList = []
    for i in range(0,50):
        probList.append(.02) # create an evenly distributed probability vector to pick each topic with 
    with open(data) as fin:
        for line in islice(fin, 1, 2): #gets the second line because the first line of the corpus I used is blank 
            currL = int(line) + 1  #set the current length to length of new document (first word of new doc is int representing word count of that document)

    currDoc = Document(docCount)
    docList.append(currDoc)

    corpus = open(corpus, 'r')
    for word in corpus.read().split():
        if len(currDoc.words) != currL: # if word is NOT the first word in a new doc
            currDoc.words.append(word)
            currDoc.total +=1 #total words in document
            nextTopic = topicsList[getNextTopic(probList, 1)] #randomly generate a topic for every word
            currDoc.topicList.append(nextTopic) #tell the document about the random assignment
            if currDoc.topics[nextTopic] == 0: #if the document has 0 assignments of the random topic, make new hash table entry 
                currDoc.topics[nextTopic] = 1
            else:
                currDoc.topics[nextTopic] += 1 # if  document has already been assigned to the topic once, increase count by 1
            if nextTopic.words[word] == 0: #if topic has’ been assigned this word before, make new hash table entry
                nextTopic.words[word] = 1 #if topic has been assigned this word, increase count by 1
                nextTopic.vocabSize += 1 #if word has not been previously assigned to topic, increase  total vocab counter
                nextTopic.entries += 1
            else:
                nextTopic.words[word] += 1
                nextTopic.entries += 1

        else: #start of new document
            docList.append(currDoc) #append the old document
            docCount = docCount + 1
            currDoc = Document(docCount) #make a new document
            currL = int(word) #set the current length to length of new document
    return docList,topicsList

def gibbs(docList, topiclist, alpha, output):
    """
    Takes in list of documents w/ topic assignments, list of topics w/ word assignments 
    returns list of documents and topics with optimized assignments, and the log likelyhood of the data if the data has converged 
    """
    checker = None #Boolean, set to True when data converges 
    for i in range (10): #does 10 Gibbs iterations
        if i > 1: #if we've done more than 1 iteration
            if checker != True: #if the data hasn't converged yet, check for convergence 
                if logLikely / prevLikely > .99: #if most recent likelihood w/i 99% of previous iteration 
                    prob = logLikely
                    checker = True  #data has converged 

        if i > 0:
            prevLikely = logLikely  #if it not the first iteration, store likelihood from previous iteration

        logLikely = 0
        for docs in docList:
            docLikely = 0
            i = 0 #index tracker
            newTopicList = []
            for word in docs.words:
                problist = [] #probability vector to be filled with 50 entries, one for each topic 
                oldTopic = docs.topicList[i] #topic word was assigned to last time
                docs.topics[oldTopic] = docs.topics[oldTopic] - 1 #decrement previous doc assignment
                if docs.topics[oldTopic] == 0:
                    del docs.topics[oldTopic] #remove doc assignment from topic if it’s 0 after we decrement 
                oldTopic.words[word] = oldTopic.words[word] - 1 #decrement previous topic assignment
                if oldTopic.words[word] == 0: #decrement topic’s total vocab size counter, if necessary 
                    oldTopic.vocabSize -= 1
                    del oldTopic.words[word]
                oldTopic.entries -= 1
                for topic in topicList:
                    delta = (docs.topics[topic] + alpha) / (docs.total + (50 * alpha)) #prob of doc given topic
                    tau =  (topic.words[word] + alpha) / (topic.entries + (topic.vocabSize * alpha)) #prob of topic given word
                    problist.append(delta * tau) #probability of this document being assigned this topic 
                    scale = sum(problist) #this is also the prob of word given document
                    docLikely += math.log(scale) #multiply the log likelyhood of each word in doc
                nextTopic = topicList[getNextTopic(problist, scale)] #assign to new topic based on new probabilities 
                newTopicList.append(nextTopic) #update topic list to reflect new assignment
                if docs.topics[nextTopic] == 0: #update docs to reflect new assignment
                    docs.topics[nextTopic] = 1
                else:
                    docs.topics[nextTopic] += 1
                if nextTopic.words[word] == 0: #update topics to reflect new assignment
                    nextTopic.words[word] = 1
                    nextTopic.vocabSize += 1
                    nextTopic.entries += 1
                else:
                    nextTopic.words[word] += 1
                    nextTopic.entries += 1
                i += 1 #when we are done with the word, increment index
            logLikely += docLikely #multiply the log likleyhood of each document
            docs.topicList = newTopicList #overwrite

    return docList, topicList, prob

def getNextTopic(prob_list, scale):
    """
    #takes in a vector of the probabilities associated with each of the 50 topics, ordered 1-50,
     and a scale representing the sum of the vector.
     returns random int representing a topic based on the prob vector
     """
    r = random.random() * scale
    n = 0 # current pointer
    i = 0 # current index
    if r == 0: return 0 #just in case
    while n < r:
        n += prob_list[i]
        i += 1
        if i == len(prob_list): break

    return i-1

class Document:
    def __init__(self, integer):
        self.integer = integer #identidy int
        self.topics = defaultdict(int)
        self.words = []
        self.topicList = [] #blank list of topics to get over written each time. Used to remove old topics
        self.total = 0

class Topic:
    def __init__(self, integer):
        self.integer = integer #idenity int
        self.words = defaultdict(int) #dict mapping words in topic to frequency of occurance
        self.entries = 0 #total entries in topic
        self.vocabSize = 0 # number of unique words in topic

if __name__ == "__main__":
    file1 = sys.argv[1] #data
    output = sys.argv[2] #output

    topicList = []
    for i in range(0,50):
        newTopic = Topic(i)
        topicList.append(newTopic) #definitely a more elegant way to write this. check the python cook book. 
    doclist, topiclist = initilize(file1, topicList) #randomly assign docs to topics and words to topics 
    gibsDocList, gibbsTopicList, prob = gibbs(doclist,topiclist, .5, output)
    output = open(output, 'w')
    output.write(str("the log likelyhood of the data at convergence is" + str(prob) + "\n" ))
    for topics in gibbsTopicList:
        output.write(str("most probable entries for topic number" +" "+ str(topics.integer) +  "\n"))
        for i, v in enumerate(sorted(topics.words.items(), key = lambda x: x[1], reverse = True)): #print the 15 most likely topics for each document 
            output.write(str(v)+ "\n")
            if i == 15: break
    output.write("PROBABILITIES OF TOPICS IN THE 17TH ARTICLE"+ "\n" ) #test the probability of the 17th article
    for topic in gibbsTopicList:
        for document in gibsDocList:
            if document.integer == 16: #if doc is the 17th document
                delta = (document.topics[topic] + .5) / (document.total + (50 * .5))
                output.write(str( "probibility of topic num." +" "+ str(topic.integer) +" "+  "is" + str(delta)+ "\n"))
