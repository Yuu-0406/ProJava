from flask import Flask, render_template, request
import osmnx as ox
import networkx as nx
import folium
from shapely.geometry import Point, LineString

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/route', methods=['POST'])
def route():
    try:
        # --- 入力値の取得 ---
        start_lat = float(request.form['start_lat'])
        start_lon = float(request.form['start_lon'])
        end_lat = float(request.form['end_lat'])
        end_lon = float(request.form['end_lon'])
        avoid_lat = float(request.form['avoid_lat'])
        avoid_lon = float(request.form['avoid_lon'])
        avoid_radius = float(request.form['avoid_radius'])  # メートル単位

        # --- 道路ネットワークを取得 ---
        G = ox.graph_from_point((start_lat, start_lon), dist=5000, network_type='drive')

        # --- 回避エリアを作成 ---
        avoid_area = Point(avoid_lon, avoid_lat).buffer(avoid_radius / 111_000)

        # --- 回避エリア内のノードを削除 ---
        G2 = G.copy()
        nodes_to_remove = []
        for node, data in G2.nodes(data=True):
            p = Point(data['x'], data['y'])
            if avoid_area.contains(p):
                nodes_to_remove.append(node)
        G2.remove_nodes_from(nodes_to_remove)

        # --- 最寄ノードを取得 ---
        orig_node = ox.distance.nearest_nodes(G2, start_lon, start_lat)
        dest_node = ox.distance.nearest_nodes(G2, end_lon, end_lat)

        # --- 経路探索 ---
        try:
            route = nx.shortest_path(G2, orig_node, dest_node, weight='length')
        except nx.NetworkXNoPath:
            return "<h3>経路が見つかりません（回避エリアが広すぎる可能性があります）。</h3>"

        # --- 経路を座標に変換 ---
        route_coords = [(G2.nodes[n]['y'], G2.nodes[n]['x']) for n in route]

        # --- folium地図を作成 ---
        m = folium.Map(location=[start_lat, start_lon], zoom_start=13)

        # 経路線を追加
        folium.PolyLine(route_coords, color='blue', weight=5, opacity=0.8, tooltip="経路").add_to(m)

        # 出発地・目的地マーカー
        folium.Marker([start_lat, start_lon], popup='出発地', icon=folium.Icon(color='green')).add_to(m)
        folium.Marker([end_lat, end_lon], popup='目的地', icon=folium.Icon(color='red')).add_to(m)

        # 回避エリア
        folium.Circle(
            location=[avoid_lat, avoid_lon],
            radius=avoid_radius,
            color='red',
            fill=True,
            fill_opacity=0.4,
            tooltip='回避エリア'
        ).add_to(m)

        # HTMLに保存
        m.save('templates/map.html')
        return render_template('map.html')

    except Exception as e:
        return f"<h2>エラー発生：</h2><p>{str(e)}</p>"

if __name__ == '__main__':
    print("☑ Flaskアプリを起動します...")
    app.run(debug=True)
