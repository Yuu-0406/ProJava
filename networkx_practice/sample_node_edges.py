import networkx as nx

G = nx.Graph() #無向グラフ
G.add_node("A")
G.add_nodes_from(["B","C"])
G.add_edge("A","B")
G.add_edges_from([("B","C"),("C","A")])

print(G.nodes())
print(G.edges())