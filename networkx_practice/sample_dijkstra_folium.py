import osmnx as ox
import networkx as nx
import folium

# ---- 1. 前橋市の道路ネットワークを取得 ----
place = "前橋市, 群馬県, 日本"
G = ox.graph_from_place(place, network_type="drive")

# ---- 2. 出発地と目的地 ----
origin_point = (36.38431, 139.07271)   # 前橋駅
destination_point = (36.43118, 139.04514)  # 群馬大学 荒牧キャンパス

# ---- 3. 近いノードを取得 ----
orig_node = ox.distance.nearest_nodes(G, X=origin_point[1], Y=origin_point[0])
dest_node = ox.distance.nearest_nodes(G, X=destination_point[1], Y=destination_point[0])

# ---- 4. 最短経路をダイクストラ法で計算 ----
route = nx.shortest_path(G, orig_node, dest_node, weight="length")

# ---- 5. folium地図を作成 ----
m = folium.Map(location=origin_point, zoom_start=13)

# ---- 6. 全道路を灰色で描画 ----
edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
for _, row in edges.iterrows():
    folium.PolyLine(locations=[(y, x) for x, y in row.geometry.coords], color="gray", weight=1).add_to(m)

# ---- 7. 経路を赤色で描画 ----
route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]
folium.PolyLine(locations=route_coords, color="red", weight=5, opacity=0.8).add_to(m)

# ---- 8. ピンを追加 ----
folium.Marker(location=origin_point, popup="前橋駅", icon=folium.Icon(color="green")).add_to(m)
folium.Marker(location=destination_point, popup="群馬大学 荒牧キャンパス", icon=folium.Icon(color="blue")).add_to(m)

# ---- 9. 保存 ----
m.save("maebashi_route.html")
print("✅ 最短経路を maebashi_route.html に保存しました。ブラウザで開いてズームできます！")
