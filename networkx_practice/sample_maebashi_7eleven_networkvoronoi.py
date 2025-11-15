import osmnx as ox
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# ==============================
# 1. 前橋市の道路ネットワークを取得
# ==============================
G = ox.graph_from_place("Maebashi, Gunma, Japan", network_type="drive")
G = ox.project_graph(G)

# ==============================
# 2. CSVファイルから店舗座標を読み込み
# ==============================
# CSVファイルを同じフォルダに保存しておく
stores_df = pd.read_csv("C:\\Users\\monja\\OneDrive\\ドキュメント\\seven_maebashi.csv", encoding='shift_jis')

# 店舗名と座標を辞書化
store_locations = dict(zip(stores_df["name"], zip(stores_df["lat"], stores_df["lon"])))

# ==============================
# 3. 各店舗を最近のノードにスナップ
# ==============================
store_nodes = {}
for name, (lat, lon) in store_locations.items():
    try:
        node = ox.distance.nearest_nodes(G, lon, lat)
        store_nodes[name] = node
    except Exception as e:
        print(f"{name} の処理中にエラー: {e}")

# ==============================
# 4. 各ノードの最寄り店舗を探索 (ネットワーク距離)
# ==============================
voronoi_assignment = {}
for node in G.nodes:
    min_dist = float("inf")
    nearest_store = None
    for name, store_node in store_nodes.items():
        try:
            dist = nx.shortest_path_length(G, node, store_node, weight="length")
            if dist < min_dist:
                min_dist = dist
                nearest_store = name
        except nx.NetworkXNoPath:
            continue
    voronoi_assignment[node] = nearest_store

# ==============================
# 5. 結果を地図として可視化
# ==============================
# ノードごとに色を割り当て
store_names = list(store_nodes.keys())
colors = cm.get_cmap('tab20', len(store_names))

node_colors = [
    colors(store_names.index(voronoi_assignment[node]) % len(store_names))
    if voronoi_assignment[node] else (0.8, 0.8, 0.8, 0.3)
    for node in G.nodes
]

fig, ax = ox.plot_graph(
    G,
    node_color=node_colors,
    node_size=5,
    edge_color="lightgray",
    bgcolor="white",
    show=False,
    close=False
)

# 店舗ノードを赤丸で表示
store_x = []
store_y = []
for name, node in store_nodes.items():
    x, y = G.nodes[node]["x"], G.nodes[node]["y"]
    store_x.append(x)
    store_y.append(y)
    ax.text(x, y, name, fontsize=6, color="black")

ax.scatter(store_x, store_y, c="red", s=20, zorder=5)
plt.title("Network Voronoi Diagram - 7-Eleven Maebashi", fontsize=12)
plt.show()
