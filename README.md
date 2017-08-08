# Gibbs-Topic-Modeler



First, I initialized the Gibbs search by randomly assigning each word in each document to a topic. Each document stores a dictionary of all the topics it has been randomly assigned to. Each topic stores a dictionary of all the words assigned to itself.  Next, I preformed Gibbs iterations. On each Gibbs iterations, each word in each document is assigned to a new topic based on the scaled respective probability of the 50 topics created during initilization. The probability of a word being assigned to topic X is the probability of the document being assigned to topic X multiplied by the probability of the word being assigned to topic X.  On every iteration after the first iteration, I checked for convergence by comparing the log likelihood of the corpus for this iteration to the likelihood of the corpus for the previous iteration. Convergence has occurred with the likelihood increases by less than 1%. 
