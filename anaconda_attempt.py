import matplotlib
matplotlib.use("TkAgg")


import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edges_from([(1,2),(1,3),(2,4)])
nx.draw(G, with_labels=True)
plt.show(block=True)