print("VS CodeからPythonが動いています!")

import matplotlib.pyplot as plt
import networkx as nx

G = nx.path_graph(5)
nx.draw(G, with_labels=True)
plt.show()