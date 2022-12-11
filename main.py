import Utils
import User
import SentimentClassifierTraining

import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
# import queue

# Graph object from networkx
G = nx.Graph()
sentiment_model = SentimentClassifierTraining.train_bayes_classifiers()
# Start generating graph from this user
initial_user_id = 17919972
# Hash table to record whether a user has been visited before
visited = set()
# Use breath first search to propagate the graph
queue = []
queue.append(initial_user_id)
visited.add(initial_user_id)

utils = Utils.Utils()
max_count = 100
# number of users
count = 0

while (len(queue) > 0 and count < max_count):
    # Select current user
    current_user_id = queue.pop(0)
    # Add current user to Graph
    G.add_node(current_user_id)

    # Fetch tweet data
    utils.set_user_id(current_user_id)
    url = utils.get_tweet_url()
    params = utils.get_params("tweet")
    json_response = utils.connect_to_endpoint(url, params)
    count += 1
    # Use current user_id as file name to save data
    with open("dataC/" + str(current_user_id) + '.json', 'w') as f:
        json.dump(json_response, f)

    # Create User object and read tweet data
    current_user = User.User(current_user_id, sentiment_model)
    current_user.save_neighbors()

    for neighbor in current_user.neighbors:
        if not (neighbor in visited):
            queue.append(neighbor)
            visited.add(neighbor)
        if not (neighbor in G.neighbors(current_user_id)) and neighbor != current_user_id:
            G.add_edge(current_user_id, neighbor)   

nx.draw(G)
plt.savefig("GraphC.png")

    # Find neighbors

    # Add neighbors to the queue
