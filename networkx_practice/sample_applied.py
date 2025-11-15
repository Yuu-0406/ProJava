import osmnx as ox
G = ox.graph_from_place("Tokyo, Japan", network_type="drive")
ox.plot_graph(G)