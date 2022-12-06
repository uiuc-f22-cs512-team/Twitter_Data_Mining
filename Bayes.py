import math
from tqdm import tqdm
from collections import Counter
import numpy as np

def print_paramter_vals(laplace, pos_prior):
    print(f"Unigram Laplace {laplace}")
    print(f"Positive prior {pos_prior}")



def generateWordDict(train_set, train_labels, isPos):
    wordDict = {}
    for i in range(len(train_set)):
        sentence = train_set[i]
        if (train_labels[i] != isPos):
            continue
        for word in sentence:
            if (word in wordDict):
                wordDict[word] = wordDict[word] + 1
            else:
                wordDict[word] = 1
    return wordDict


def calculateProb(wordMap, laplace):
    probMap = {}
    n_type = len(wordMap)
    n_token = 0
    for word in wordMap:
        n_token += wordMap[word]

    for word in wordMap:
        prob = (wordMap[word] + laplace)/(n_token + laplace*(n_type+1))
        probMap[word] = prob

    unk_prob = laplace/(n_token + laplace*(n_type+1))

    return probMap, unk_prob


def naiveBayes(train_set, train_labels, dev_set, laplace=0.01, pos_prior=0.95, silently=False):
    print_paramter_vals(laplace, pos_prior)
    positiveWordMap = generateWordDict(train_set, train_labels, 1)
    negativeWordMap = generateWordDict(train_set, train_labels, 0)

    positiveProbMap, positive_unk_prob = calculateProb(positiveWordMap, laplace)
    negativeProbMap, negative_unk_prob = calculateProb(negativeWordMap, laplace)

    yhats = []
    for doc in tqdm(dev_set, disable=silently):
        pos_prob = math.log(pos_prior)
        neg_prob = math.log(1-pos_prior)

        for word in doc:
            if word in positiveProbMap:
                pos_prob += math.log(positiveProbMap[word])
            else:
                pos_prob += math.log(positive_unk_prob)

            if word in negativeProbMap:
                neg_prob += math.log(negativeProbMap[word])
            else:
                neg_prob += math.log(negative_unk_prob)

        if (pos_prob >= neg_prob):
            yhats.append(1)
        else:
            yhats.append(0)
    return yhats


def print_paramter_vals_bigram(unigram_laplace, bigram_laplace, bigram_lambda, pos_prior):
    print(f"Unigram Laplace {unigram_laplace}")
    print(f"Bigram Laplace {bigram_laplace}")
    print(f"Bigram Lambda {bigram_lambda}")
    print(f"Positive prior {pos_prior}")


"""
You can modify the default values for the Laplace smoothing parameters, model-mixture lambda parameter, and the prior for the positive label.
Notice that we may pass in specific values for these parameters during our testing.
"""

# main function for the bigrammixture model

def generateBigramDict(train_set, train_labels, isPos):
    bigramDict = {}
    for i in range(len(train_labels)):
        sentence = train_set[i]
        if (train_labels[i] != isPos):
            continue
        for j in range(len(sentence)-1):
            bigram = (sentence[j], sentence[j+1])

            if (bigram in bigramDict):
                bigramDict[bigram] = bigramDict[bigram] + 1
            else:
                bigramDict[bigram] = 1
    return bigramDict

def bigramBayes(train_set, train_labels, dev_set, unigram_laplace=0.001, bigram_laplace=0.005, bigram_lambda=0.5, pos_prior=0.95, silently=False):
    print_paramter_vals_bigram(
        unigram_laplace, bigram_laplace, bigram_lambda, pos_prior)

    # unigram
    positiveWordMap = generateWordDict(train_set, train_labels, 1)
    negativeWordMap = generateWordDict(train_set, train_labels, 0)

    positiveProbMap, positive_unk_prob = calculateProb(positiveWordMap, unigram_laplace)
    negativeProbMap, negative_unk_prob = calculateProb(negativeWordMap, unigram_laplace)

    pos_uni_score = []
    neg_uni_score = []
    for doc in tqdm(dev_set, disable=silently):
        pos_prob = math.log(pos_prior)
        neg_prob = math.log(1-pos_prior)

        for word in doc:
            if word in positiveProbMap:
                pos_prob += math.log(positiveProbMap[word])
            else:
                pos_prob += math.log(positive_unk_prob)

            if word in negativeProbMap:
                neg_prob += math.log(negativeProbMap[word])
            else:
                neg_prob += math.log(negative_unk_prob)
        pos_uni_score.append(pos_prob)
        neg_uni_score.append(neg_prob)

    # bigram
    positiveBigramMap = generateBigramDict(train_set, train_labels, 1)
    negativeBigramMap = generateBigramDict(train_set, train_labels, 0)

    positiveBigramProbMap, positive_bigram_unk_prob = calculateProb(positiveBigramMap, bigram_laplace)
    negativeBigramProbMap, negative_bigram_unk_prob = calculateProb(negativeBigramMap, bigram_laplace)
    
    yhats = []
    pos_bi_score = []
    neg_bi_score = []
    
    for doc in tqdm(dev_set, disable=silently):
        pos_prob = math.log(pos_prior)
        neg_prob = math.log(1-pos_prior)
        
        for j in range(len(doc)-1):
            bigram = (doc[j], doc[j+1])
            if bigram in positiveBigramProbMap:
                pos_prob += math.log(positiveBigramProbMap[bigram])
            else:
                pos_prob += math.log(positive_bigram_unk_prob)

            if bigram in negativeBigramProbMap:
                neg_prob += math.log(negativeBigramProbMap[bigram])
            else:
                neg_prob += math.log(negative_bigram_unk_prob)
        pos_bi_score.append(pos_prob)
        neg_bi_score.append(neg_prob)

    # mixture
    for i in range(len(pos_uni_score)):
        pos_prob = (1-bigram_lambda)*pos_uni_score[i] + (bigram_lambda)*pos_bi_score[i]
        neg_prob = (1-bigram_lambda)*neg_uni_score[i] + (bigram_lambda)*neg_bi_score[i]
        if (pos_prob >= neg_prob):
            yhats.append(1)
        else:
            yhats.append(0)

    return yhats
