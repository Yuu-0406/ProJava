import matplotlib.pyplot as plt
import networkx as nx

G = nx.DiGraph()
nx.add_cyle(G,[1,2,3,4,5])
nx.add_star(G,[1,2,3,4,5])

print(list(G.nodes))

print(list(G.edges))

print(list(G.succ[1]), G.out_edges(1))

print(list(G.pred[5]), G.in_edges(5))

print(G.degree(4), list(nx.all_neighbors(G,4)))