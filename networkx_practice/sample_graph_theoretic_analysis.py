import networkx as nx
G = nx.Graph()

print(nx.degree_centrality(G))
print(nx.betweenness_centrality(G))
print(nx.shortest_path(G, source="A", target="C"))