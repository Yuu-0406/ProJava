import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1000)
plt.show()

#目標:自分の好みのネットワーク図を描けるようにする