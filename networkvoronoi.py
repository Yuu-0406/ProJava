import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
# import time

G = nx.DiGraph()

G.add_node(1)
G.add_nodes_from([3,4,5])
G.add_edge(1,2)
G.add_edges_from([(1,3),(2,5),(3,4),(4,5)])

print("Nodes:", G.nodes())
print("Edges:", G.edges())

nx.draw(G, with_labels=True, node_color="lightblue",arrows=True)
plt.show()

# time.sleep(500)

G.remove_edge(3,4)
G.remove_edges_from([(1,3),(2,5)])
G.remove_node(5)
G.remove_nodes_from([3,4])
nx.add_path(G,[1,2,3,4,5])
nx.add_cycle(G,[1,2,3,4,5])
nx.add_star(G,[1,2,3,4,5])

nx.draw(G, with_labels=True, node_color="lightblue",arrows=True)
plt.show()
# time.sleep(500)


