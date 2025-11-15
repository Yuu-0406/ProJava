import osmnx as ox

G = ox.graph_from_place("前橋市, 群馬県, 日本", network_type="drive")

import os
os.makedirs("data", exist_ok=True)

ox.save_graphml(G, "data/maebashi_graph.graphml")
print("☑ 前橋市の道路ネットワークを data/maebashi_graph.graphmlに保存しました。")
