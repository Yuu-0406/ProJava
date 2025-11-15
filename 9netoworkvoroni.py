import matplotlib.pyplot as plt
import networkx as nx

G = nx.DiGraph()
nx.add_path(G, [3,5,4,1,0,2,7,8,9,6])
nx.add_path(G, [3,0,6,4,2,7,1,9,8,5])
nx.add_path(G, [1,3,5,7,6,0,9,8,2,4])
nx.add_path(G, [4,6,0,5,7,3,9,2,8,1])

nx.draw_networkx(G)
plt.show()