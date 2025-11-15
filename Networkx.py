import networkx as nx

G = nx.DiGraph()

G.add_node(1)
G.add_nodes_from([2,3,4,5])

G.add_edge(1,2)
G.add_edges_from([(2,3),(3,4),(4,5),(5,1)])

print("ノード一覧:", G.nodes())
print("エッジ一覧:", G.edges())
print("ノード数:", G.number_of_nodes())
print("エッジ数:", G.number_of_edges())