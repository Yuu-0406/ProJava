from flask import Flask, render_template, request
import osmnx as ox
import networkx as nx
import folium
from shapely.geometry import LineString

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
    # 現在地（固定）
    start_lat = 36.4253
    start_lon = 139.0527
    
    # 目的地（GETパラメータから取得、デフォルト値あり）
    end_lat = float(request.args.get("end_lat", 36.3894))
    end_lon = float(request.args.get("end_lon", 139.0636))
    
    # 最寄りノードを取得
    orig_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
    dest_node = ox.distance.nearest_nodes(G, end_lon, end_lat)
    
    # 最短経路を計算（道路選択用）
    try:
        route_nodes = nx.shortest_path(G, orig_node, dest_node, weight="length")
    except nx.NetworkXNoPath:
        return "<h3>経路が見つかりません</h3>"
    
    # 経路のLineStringを作成（バッファ計算用）
    route_coords_list = []
    for i in range(len(route_nodes) - 1):
        u = route_nodes[i]
        v = route_nodes[i + 1]
        edge_data = G.get_edge_data(u, v, 0)
        if edge_data and "geometry" in edge_data:
            edge_coords = list(edge_data["geometry"].coords)
            # 最初のエッジ以外は、最初の座標をスキップ（重複を避ける）
            if i > 0 and route_coords_list:
                route_coords_list.extend(edge_coords[1:])
            else:
                route_coords_list.extend(edge_coords)
        else:
            if i == 0:
                route_coords_list.append((G.nodes[u]["x"], G.nodes[u]["y"]))
            route_coords_list.append((G.nodes[v]["x"], G.nodes[v]["y"]))
    
    # 経路のLineStringを作成
    route_linestring = LineString(route_coords_list)
    
    # 経路周辺のバッファ（500メートル）を作成
    buffer_distance = 500  # メートル
    route_buffer = route_linestring.buffer(buffer_distance / 111000)  # 度に変換（おおよそ）
    
    # バッファ内にあるエッジのみを抽出
    nearby_edges = set()
    for u, v, k, data in G.edges(keys=True, data=True):
        if "geometry" in data:
            edge_geom = data["geometry"]
        else:
            edge_geom = LineString([(G.nodes[u]["x"], G.nodes[u]["y"]),
                                   (G.nodes[v]["x"], G.nodes[v]["y"])])
        
        # エッジがバッファと交差するか、バッファ内にあるかチェック
        if route_buffer.intersects(edge_geom) or route_buffer.contains(edge_geom):
            nearby_edges.add((u, v, k))
    
    # Folium地図作成
    center_lat = (start_lat + end_lat) / 2
    center_lon = (start_lon + end_lon) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
    
    # 最短経路に含まれるエッジを特定（選択対象外にするため）
    # ノードの組み合わせで判定（キーは無視）
    route_node_pairs = set()
    for i in range(len(route_nodes) - 1):
        u = route_nodes[i]
        v = route_nodes[i + 1]
        route_node_pairs.add((u, v))
        route_node_pairs.add((v, u))  # 双方向を考慮
    
    # 経路周辺の道路のみを描画
    for u, v, k in nearby_edges:
        data = G.get_edge_data(u, v, k)
        if "geometry" in data:
            coords = [(p[1], p[0]) for p in data["geometry"].coords]
        else:
            coords = [(G.nodes[u]["y"], G.nodes[u]["x"]),
                      (G.nodes[v]["y"], G.nodes[v]["x"])]
        
        # 最短経路に含まれるエッジかどうかを判定
        # ノードの組み合わせで判定（キーは無視）
        is_route_edge = (u, v) in route_node_pairs
        
        edge_id = f"{u}-{v}-{k}"
        if is_route_edge:
            # 最短経路のエッジは緑色で表示（選択対象外）
            # popupにエッジIDを含めて、JavaScriptで取得できるようにする
            folium.PolyLine(
                coords,
                color="green",
                weight=6,
                opacity=0.8,
                tooltip=f"最短経路エッジ {edge_id}",
                popup=folium.Popup(f"最短経路: {edge_id}", parse_html=False)
            ).add_to(m)
        else:
            # 通常の道路は青色で表示（選択可能）
            # popupにエッジIDを含めて、JavaScriptで取得できるようにする
            folium.PolyLine(
                coords,
                color="blue",
                weight=4,
                opacity=0.7,
                tooltip=f"Edge {edge_id}",
                popup=folium.Popup(f"道路: {edge_id}", parse_html=False)
            ).add_to(m)
    
    # 現在地と目的地のマーカーを表示
    folium.Marker([start_lat, start_lon], popup="現在地", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker([end_lat, end_lon], popup="目的地", icon=folium.Icon(color="red")).add_to(m)
    
    # エッジIDのマッピングをJavaScriptに渡すためのスクリプトを追加
    # DOM要素から直接処理する方法（マップオブジェクトに依存しない）
    edge_mapping_script = '''
    <script>
        (function() {
            let handlersSetup = false; // 重複設定を防ぐフラグ
            
            function setupEdgeClickHandlers() {
                // 既に設定済みの場合はスキップ
                if (handlersSetup) {
                    return;
                }
                
                console.log("エッジクリックハンドラーを設定中...");
                
                // 地図コンテナを取得
                const mapContainer = document.querySelector('.folium-map');
                if (!mapContainer) {
                    console.log("地図コンテナが見つかりません。再試行します...");
                    setTimeout(setupEdgeClickHandlers, 500);
                    return;
                }
                
                // SVGパス要素を取得
                const paths = mapContainer.querySelectorAll('svg path.leaflet-interactive');
                console.log(`見つかったパス要素数: ${paths.length}`);
                
                if (paths.length === 0) {
                    console.log("パス要素が見つかりません。再試行します...");
                    setTimeout(setupEdgeClickHandlers, 500);
                    return;
                }
                
                // 各パス要素にイベントリスナーを設定
                let setupCount = 0;
                paths.forEach(function(path) {
                    // 既に設定済みの場合はスキップ
                    if (path.hasAttribute('data-handler-set')) {
                        return;
                    }
                    
                    // 設定済みフラグを設定
                    path.setAttribute('data-handler-set', 'true');
                    
                    // マウスオーバー時にtooltipからエッジIDを取得
                    path.addEventListener('mouseenter', function() {
                        const pathElement = this;
                        setTimeout(function() {
                            const tooltip = document.querySelector('.leaflet-tooltip');
                            if (tooltip) {
                                const text = tooltip.textContent || tooltip.innerText;
                                let edgeId = null;
                                let isRouteEdge = false;
                                
                                // "Edge 123-456-0" の形式
                                const edgeMatch = text.match(/Edge\s+(\d+-\d+-\d+)/);
                                if (edgeMatch) {
                                    edgeId = edgeMatch[1];
                                    isRouteEdge = false;
                                }
                                
                                // "最短経路エッジ 123-456-0" の形式
                                const routeMatch = text.match(/最短経路エッジ\s+(\d+-\d+-\d+)/);
                                if (routeMatch) {
                                    edgeId = routeMatch[1];
                                    isRouteEdge = true;
                                }
                                
                                if (edgeId) {
                                    pathElement.setAttribute('data-edge-id', edgeId);
                                    pathElement.setAttribute('data-route-edge', isRouteEdge.toString());
                                    console.log(`パス要素にエッジIDを設定: ${edgeId}, isRoute: ${isRouteEdge}`);
                                }
                            }
                        }, 100);
                    });
                    
                    // クリックイベント
                    path.addEventListener('click', function(e) {
                        e.stopPropagation();
                        e.preventDefault();
                        
                        const edgeId = this.getAttribute('data-edge-id');
                        const isRouteEdge = this.getAttribute('data-route-edge') === 'true';
                        
                        console.log("パス要素がクリックされました:", {
                            edgeId: edgeId,
                            isRouteEdge: isRouteEdge,
                            element: this
                        });
                        
                        if (edgeId && window.handleEdgeClick) {
                            window.handleEdgeClick(edgeId, isRouteEdge, null);
                        } else if (!edgeId) {
                            console.log("エッジIDが設定されていません。マウスオーバーしてからクリックしてください。");
                        }
                    });
                    
                    setupCount++;
                });
                
                if (setupCount > 0) {
                    handlersSetup = true;
                    console.log(`エッジクリックハンドラーの設定が完了しました。処理したパス要素数: ${setupCount}`);
                } else {
                    console.log("新しいパス要素が見つかりませんでした");
                }
            }
            
            // 地図が読み込まれた後に実行（複数回試行）
            setTimeout(setupEdgeClickHandlers, 1000);
            setTimeout(setupEdgeClickHandlers, 2000);
            setTimeout(setupEdgeClickHandlers, 3000);
            
            // 地図の更新を監視（動的に追加される要素に対応）
            const observer = new MutationObserver(function(mutations) {
                if (!handlersSetup) {
                    setupEdgeClickHandlers();
                }
            });
            
            // 地図コンテナの変更を監視
            setTimeout(function() {
                const mapContainer = document.querySelector('.folium-map');
                if (mapContainer) {
                    observer.observe(mapContainer, {
                        childList: true,
                        subtree: true
                    });
                }
            }, 2000);
        })();
    </script>
    '''
    m.get_root().html.add_child(folium.Element(edge_mapping_script))

    return render_template("map_select.html", m=m._repr_html_(), start_lat=start_lat, start_lon=start_lon, end_lat=end_lat, end_lon=end_lon)


# ------------------------
# 最短経路計算
# ------------------------
@app.route("/route", methods=["POST"])
def route():
    try:
        # 現在地（フォーム入力、デフォルト値あり）
        start_lat = float(request.form.get("start_lat", 36.4253))
        start_lon = float(request.form.get("start_lon", 139.0527))

        # 目的地（フォーム入力）
        end_lat = float(request.form["end_lat"])
        end_lon = float(request.form["end_lon"])

        # 回避リンクをフォームから取得（カンマ区切り）
        print("=== フォームデータ受信 ===")
        print(f"全フォームデータ: {dict(request.form)}")
        avoid_edges_raw = request.form.get("avoid_edges", "")
        print(f"avoid_edges_raw (受信値): '{avoid_edges_raw}'")
        print(f"avoid_edges_raw の型: {type(avoid_edges_raw)}")
        print(f"avoid_edges_raw の長さ: {len(avoid_edges_raw)}")
        
        avoid_edges_list = [eid.strip() for eid in avoid_edges_raw.split(",") if eid.strip()] if avoid_edges_raw else []
        
        print(f"回避リンク数: {len(avoid_edges_list)}")
        print(f"回避リンク: {avoid_edges_list}")

        # グラフコピーして回避リンク削除
        G2 = G.copy()
        removed_count = 0
        for eid in avoid_edges_list:
            try:
                u, v, k = eid.split("-")
                u, v, k = int(u), int(v), int(k)
                # エッジが存在するか確認
                if G2.has_edge(u, v, k):
                    G2.remove_edge(u, v, k)
                    removed_count += 1
                    print(f"回避リンク削除成功: {u}-{v}-{k}")
                else:
                    print(f"回避リンクが存在しません: {u}-{v}-{k}")
            except Exception as e:
                print(f"削除失敗 ({eid}): {e}")
        
        print(f"実際に削除されたエッジ数: {removed_count}")

        # 最寄りノード
        orig_node = ox.distance.nearest_nodes(G2, start_lon, start_lat)
        dest_node = ox.distance.nearest_nodes(G2, end_lon, end_lat)

        # 元のグラフでの最短経路を計算（比較用）
        orig_orig_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
        orig_dest_node = ox.distance.nearest_nodes(G, end_lon, end_lat)
        try:
            original_route_nodes = nx.shortest_path(G, orig_orig_node, orig_dest_node, weight="length")
            original_route_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in original_route_nodes]
        except nx.NetworkXNoPath:
            original_route_coords = []

        # 経路探索（回避リンク削除後）
        route_nodes = nx.shortest_path(G2, orig_node, dest_node, weight="length")

        # 経路座標
        route_coords = [(G2.nodes[n]["y"], G2.nodes[n]["x"]) for n in route_nodes]

        # Folium 地図作成
        center_lat = (start_lat + end_lat) / 2
        center_lon = (start_lon + end_lon) / 2
        m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
        
        # 元の最短経路を表示（青色、破線）
        if original_route_coords:
            # 経路の距離を計算
            original_distance = 0
            for i in range(len(original_route_nodes) - 1):
                u = original_route_nodes[i]
                v = original_route_nodes[i + 1]
                edge_data = G.get_edge_data(u, v, 0)
                if edge_data:
                    original_distance += edge_data.get('length', 0)
            original_distance_km = original_distance / 1000
            folium.PolyLine(
                original_route_coords, 
                color="blue", 
                weight=5, 
                opacity=0.7, 
                tooltip=f"元の最短経路 ({original_distance_km:.2f} km)",
                popup=f"元の最短経路: {original_distance_km:.2f} km"
            ).add_to(m)
        
        # 回避リンク削除後の経路を表示（赤色、太線）
        # 経路の距離を計算
        route_distance = 0
        for i in range(len(route_nodes) - 1):
            u = route_nodes[i]
            v = route_nodes[i + 1]
            edge_data = G2.get_edge_data(u, v, 0)
            if edge_data:
                route_distance += edge_data.get('length', 0)
        route_distance_km = route_distance / 1000
        folium.PolyLine(
            route_coords, 
            color="red", 
            weight=7, 
            opacity=0.9, 
            tooltip=f"回避経路 ({route_distance_km:.2f} km)",
            popup=f"回避経路: {route_distance_km:.2f} km"
        ).add_to(m)
        
        # 凡例を追加
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 220px; height: 120px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.3)">
        <h4 style="margin-top:0; margin-bottom:10px">凡例</h4>
        <p style="margin:5px 0"><span style="display:inline-block; width:20px; height:5px; background-color:blue; vertical-align:middle; margin-right:8px"></span> 元の最短経路</p>
        <p style="margin:5px 0"><span style="display:inline-block; width:20px; height:7px; background-color:red; vertical-align:middle; margin-right:8px"></span> 回避経路</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        folium.Marker([start_lat, start_lon], popup="出発地", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker([end_lat, end_lon], popup="目的地", icon=folium.Icon(color="red")).add_to(m)

        # 経路情報をテンプレートに渡す
        route_info = {
            "original_distance_km": original_distance_km if original_route_coords else None,
            "avoid_distance_km": route_distance_km,
            "avoid_edges_count": len(avoid_edges_list)
        }
        
        return render_template("map.html", m=m._repr_html_(), route_info=route_info)
    except nx.NetworkXNoPath:
        return "<h3>回避道路が多すぎて経路が見つかりません</h3>"
    except Exception as e:
        return f"<h3>エラー: {e}</h3>"


if __name__ == "__main__":
    print("Flask 起動中 http://127.0.0.1:5000")
    app.run(debug=True)
