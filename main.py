import Utils
import User

import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
# import queue

# Graph object from networkx
G = nx.Graph()

# Start generating graph from this user
initial_user_id = 44196397
# Hash table to record whether a user has been visited before
visited = set()
# Use breath first search to propagate the graph
queue = []
queue.append(initial_user_id)
visited.add(initial_user_id)

utils = Utils.Utils()
max_vertices = 30

while (len(queue) > 0 and G.number_of_nodes() < max_vertices):
    # Select current user
    current_user_id = queue.pop(0)
    # Add current user to Graph
    G.add_node(current_user_id)

    # Fetch tweet data
    utils.set_user_id(current_user_id)
    url = utils.get_tweet_url()
    params = utils.get_params("tweet")
    json_response = utils.connect_to_endpoint(url, params)
    # Use current user_id as file name to save data
    with open("data/" + str(current_user_id) + '.json', 'w') as f:
        json.dump(json_response, f)

    # Create User object and read tweet data
    current_user = User.User(current_user_id)
    current_user.save_neighbors()

    for neighbor in current_user.neighbors:
        if not (neighbor in visited):
            queue.append(neighbor)
            visited.add(neighbor)
        if not (neighbor in G.neighbors(current_user_id)) and neighbor != current_user_id:
            G.add_edge(current_user_id, neighbor)   

nx.draw(G, with_label=True)
plt.savefig("TestGraph.png")

    # Find neighbors

    # Add neighbors to the queue
