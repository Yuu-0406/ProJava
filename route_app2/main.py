from flask import Flask, render_template, request
import osmnx as ox
import networkx as nx
import folium

app = Flask(__name__)

# ------------------------
# 前橋市道路ネットワークを一度だけロード
# ------------------------
GRAPH_PATH = "data/maebashi_graph.graphml"
print("Loading graph:", GRAPH_PATH)
G = ox.load_graphml(GRAPH_PATH)

# ------------------------
# トップページ
# ------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ------------------------
# 道路選択ページ
# ------------------------
@app.route("/select_road")
def select_road():
    # folium で全道路描画
    m = folium.Map(location=[36.390, 139.060], zoom_start=13)

    for u, v, k, data in G.edges(keys=True, data=True):
        if "geometry" in data:
            coords = [(p[1], p[0]) for p in data["geometry"].coords]
        else:
            coords = [(G.nodes[u]["y"], G.nodes[u]["x"]),
                      (G.nodes[v]["y"], G.nodes[v]["x"])]
        folium.PolyLine(
            coords,
            color="blue",
            weight=4,
            opacity=0.7,
            tooltip=f"Edge {u}-{v}-{k}",
            **{"data-edge-id": f"{u}-{v}-{k}"}
        ).add_to(m)

    return render_template("map_select.html", m=m._repr_html_())


# ------------------------
# 最短経路計算
# ------------------------
@app.route("/route", methods=["POST"])
def route():
    try:
        # 出発地（固定）
        start_lat = 36.4253
        start_lon = 139.0527

        # 目的地（フォーム入力）
        end_lat = float(request.form["end_lat"])
        end_lon = float(request.form["end_lon"])

        # 回避リンクをフォームから取得（カンマ区切り）
        avoid_edges_raw = request.form.get("avoid_edges", "")
        avoid_edges_list = avoid_edges_raw.split(",") if avoid_edges_raw else []

        # グラフコピーして回避リンク削除
        G2 = G.copy()
        for eid in avoid_edges_list:
            try:
                u, v, k = eid.split("-")
                u, v, k = int(u), int(v), int(k)
                G2.remove_edge(u, v, k)
            except Exception as e:
                print("削除失敗:", e)

        # 最寄りノード
        orig_node = ox.distance.nearest_nodes(G2, start_lon, start_lat)
        dest_node = ox.distance.nearest_nodes(G2, end_lon, end_lat)

        # 経路探索
        route_nodes = nx.shortest_path(G2, orig_node, dest_node, weight="length")

        # 経路座標
        route_coords = [(G2.nodes[n]["y"], G2.nodes[n]["x"]) for n in route_nodes]

        # Folium 地図作成
        m = folium.Map(location=[start_lat, start_lon], zoom_start=13)
        folium.PolyLine(route_coords, color="green", weight=6, opacity=0.8, tooltip="経路").add_to(m)
        folium.Marker([start_lat, start_lon], popup="出発地", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker([end_lat, end_lon], popup="目的地", icon=folium.Icon(color="red")).add_to(m)

        return render_template("map.html", m=m._repr_html_())
    except nx.NetworkXNoPath:
        return "<h3>回避道路が多すぎて経路が見つかりません</h3>"
    except Exception as e:
        return f"<h3>エラー: {e}</h3>"


if __name__ == "__main__":
    print("Flask 起動中 http://127.0.0.1:5000")
    app.run(debug=True)
