import numpy as np
import csv

def load_tweets(path, order):
    Transactions = []
    with open(path, "r") as items:
        for line in items:
            transaction = list(line.strip().split(','))
            transaction.sort(key=lambda x: order.index(x))
            Transactions.append(transaction)
    return Transactions

def compute_rel_support(itemset, Transactions):
    count = 0
    for i in range(len(Transactions)):
        if set(itemset).issubset(set(Transactions[i])):
            count += 1
    return count

def find_frequent_itemsets(itemsets, Transactions, min_sup, pruned):
    frequent_set_tuple = [] # [(itemset, rel_sup)]
    new_pruned = []
    kp = len(pruned.keys())

    for i in range(len(itemsets)):
        # Remove itemsets that are alread pruned
        removed = False
        for itemset in pruned[kp]:
            if set(itemset).issubset(set(itemsets[i])):
                removed = True
                break # out of the pruned loop

        if not removed: # check for frequency
            rel_sup = compute_rel_support(itemsets[i], Transactions)
            if rel_sup >= min_sup: # min_sup is 1264
                t = (itemsets[i], rel_sup)
                frequent_set_tuple.append(t)
            else:
                new_pruned.append(itemsets[i])

    return frequent_set_tuple, new_pruned

def join_itemsets(itemsets, order):
    candidate_list = []
    for i in range(len(itemsets)):
        for j in range(i + 1, len(itemsets)):
            # join the itemsets
            itemsets[i].sort(key=lambda x: order.index(x))
            itemsets[j].sort(key=lambda x: order.index(x))
            itemsets_joined = []
            can_join = True
            for k in range(len(itemsets[i]) - 1):
                if itemsets[i][k] != itemsets[j][k]:
                    can_join = False
                    break 
            if can_join and order.index(itemsets[i][-1]) < order.index(itemsets[j][-1]):
                itemsets_joined = itemsets[i] + [itemsets[j][-1]] # add the last element of the itemset[j]
            if len(itemsets_joined) > 0:
                candidate_list.append(itemsets_joined)

    return candidate_list

def find_unique_words(path):
    unique_words = []
    with open(path, 'r') as file:
        rows = csv.reader(file, delimiter=',')
        for row in rows:
            unique_items = set(val for val in row)
            for item in unique_items:
                if item not in unique_words:
                    unique_words.append(item)
    return unique_words

def init_minsup(path, ratio=0.01):
    num_of_words = 0
    with open(path, 'r') as file:
        for line in file:
            num_of_words += line.count(',')
    minsup = int(num_of_words * ratio)
    return minsup

def run(path='data/tweets_history.csv', minsup=230):
    # initialization
    order = find_unique_words(path)
    Transactions = load_tweets(path, order)
    minsup = init_minsup(path)
    candidates = {}
    frequent_set = {} # k-frequent_set
    k = 1
    candidates.update({k : [ [f] for f in order]})
    pruned = {k: []}
    freq_set, new_pruned = find_frequent_itemsets(candidates[k], Transactions, minsup, pruned) 
    pruned.update({k : new_pruned})
    frequent_set.update({k : freq_set})

    # run apriori
    k = 2
    frequent_itemsets = [item[0] for item in frequent_set[k-1]] # frequent 1-itemsets
    conv = False
    while not conv:
        candidates.update({k : join_itemsets(frequent_itemsets, order)})
        freq_set, new_pruned = find_frequent_itemsets(candidates[k], Transactions, minsup, pruned) 
        frequent_set.update({k: freq_set})
        #print(frequent_itemsets) 
        pruned.update({k: new_pruned})
        if len(frequent_set[k]) == 0:
            conv = True
        k += 1
        frequent_itemsets = [item[0] for item in frequent_set[k-1]] # frequent k-itemsets

    return frequent_set # result
