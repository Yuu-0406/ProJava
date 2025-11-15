import osmnx as ox

ox.settings.log_console = True
G = ox.graph_from_place("Maebashi, Gunma, Japan", network_type="drive")
ox.plot_graph(G)