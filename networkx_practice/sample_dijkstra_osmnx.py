#前橋駅から群馬大学への最短経路探索(ダイクストラ)

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# 対象地域を設定（ここでは前橋市）
place_name = "Maebashi, Gunma, Japan"

# OpenStreetMapから道路ネットワークを取得（車用の道路）
G = ox.graph_from_place(place_name, network_type="drive")

# 任意の2点（緯度・経度）を設定
# 前橋駅と群馬大学（荒牧キャンパス）付近の例
origin_point = (36.389, 139.072)  # Maebashi Station
destination_point = (36.427, 139.020)  # Gunma University Aramaki

# 最も近いノード（道路上の点）を探す
orig_node = ox.distance.nearest_nodes(G, X=origin_point[1], Y=origin_point[0])
dest_node = ox.distance.nearest_nodes(G, X=destination_point[1], Y=destination_point[0])

# ダイクストラ法で最短経路を計算（距離を重みとして）
route = nx.shortest_path(G, orig_node, dest_node, weight='length', method='dijkstra')

# 地図上に描画
fig, ax = ox.plot_graph_route(G, route, route_linewidth=4, node_size=0, bgcolor='white')
plt.show()
