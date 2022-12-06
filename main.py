import Utils
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
# import queue

# Need a data structure to store the graph or use networkx
G = nx.DiGraph()
initial_user = 44196397
queue = []
queue.append(initial_user)
max_vertices = 1000
# Use breath first search to propagate the graph
while (queue.length > 0):
    current_user = queue.pop(0)
    # Fetch information data

    # Find neighbors

    # Add neighbors to the queue
