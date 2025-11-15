import osmnx as ox
import networkx as nx
import folium
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# ---- 1. 前橋市の道路ネットワークを取得 ----
place = "前橋市, 群馬県, 日本"
G = ox.graph_from_place(place, network_type="drive")

# ---- 2. セブンイレブン店舗座標 ----
stores = {
    "本町一丁目": (36.3919, 139.0636),
    "広瀬三丁目": (36.3687, 139.0829),
    "表町二丁目": (36.3897, 139.0720),
    "元総社町": (36.3936, 139.0279),
    "市民文化会館前": (36.3792, 139.0674),
    "大渡町": (36.4001, 139.0415),
    "小相木町": (36.3927, 139.0709),
    "古市町": (36.3955, 139.0562)
}

# ---- 3. 店舗に最も近い道路ノードを取得 ----
store_nodes = {name: ox.distance.nearest_nodes(G, X=lon, Y=lat) for name, (lat, lon) in stores.items()}

# ---- 4. 高速化：各店舗から全ノードまでの最短距離を一括計算 ----
store_distances = {}
for store_name, store_node in store_nodes.items():
    lengths = nx.single_source_dijkstra_path_length(G, store_node, weight='length')
    store_distances[store_name] = lengths

# ---- 5. 各ノードに最も近い店舗を割り当てる ----
node_owner = {}
for node in G.nodes:
    min_dist = float('inf')
    closest_store = None
    for store_name, lengths in store_distances.items():
        dist = lengths.get(node, float('inf'))
        if dist < min_dist:
            min_dist = dist
            closest_store = store_name
    node_owner[node] = closest_store

# ---- 6. Folium 地図作成 ----
center = (sum([G.nodes[n]['y'] for n in G.nodes])/len(G.nodes),
          sum([G.nodes[n]['x'] for n in G.nodes])/len(G.nodes))
m = folium.Map(location=center, zoom_start=13)

# ---- 7. 店舗ごとに色を割り当て ----
store_names = list(stores.keys())
cmap = cm.get_cmap('tab10', len(store_names))
colors = {name: mcolors.to_hex(cmap(i)) for i, name in enumerate(store_names)}

# ---- 8. 道路を描画（同じ店舗に属する道路のみ色分け） ----
edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
for idx, row in edges.iterrows():
    # 最新OSMnxでは u,v はインデックスの最初2階層に格納
    u, v = idx[0], idx[1]
    owner_u = node_owner.get(u)
    owner_v = node_owner.get(v)
    if owner_u == owner_v:  # 同じ店舗に属する道路のみ描画
        folium.PolyLine(
            locations=[(y, x) for x, y in row.geometry.coords],
            color=colors.get(owner_u, "gray"),
            weight=2,
            opacity=0.7
        ).add_to(m)

# ---- 9. 店舗マーカーを追加 ----
for name, (lat, lon) in stores.items():
    folium.Marker(
        location=(lat, lon),
        popup=name,
        icon=folium.Icon(color='white', icon_color=colors[name])
    ).add_to(m)

# ---- 10. 保存 ----
m.save("network_voronoi_fast.html")
print("✅ 高速化＋最新OSMnx対応版ネットワークボロノイ図を network_voronoi_fast.html に保存しました")
