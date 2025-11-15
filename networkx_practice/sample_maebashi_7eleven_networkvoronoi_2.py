#前橋市のセブンイレブン全店舗のネットワークボロノイ図の作成

# maebashi_7eleven_voronoi_html.py
import os
import sys
import pandas as pd
import osmnx as ox
import networkx as nx
import folium
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# ---------- 設定 ----------
CSV_PATH = r"C:\Users\monja\OneDrive\ドキュメント\seven_maebashi.csv"  # 既存CSVのフルパス or 相対パス
OUT_HTML = "maebashi_7eleven_voronoi.html"
PLACE = "前橋市, 群馬県, 日本"

# ---------- CSV 読み込み（Shift-JIS をまず試す） ----------
encodings_to_try = ["shift_jis", "utf-8", "cp932"]
stores_df = None
for enc in encodings_to_try:
    try:
        stores_df = pd.read_csv(CSV_PATH, encoding=enc)
        print(f"CSV 読み込み成功 (encoding={enc})")
        break
    except FileNotFoundError:
        print(f"CSVファイルが見つかりません: {CSV_PATH}")
        sys.exit(1)
    except Exception as e:
        print(f"encoding={enc} で読み込み失敗: {e}")
if stores_df is None:
    print("CSVの読み込みに失敗しました。エンコーディングを確認してください。")
    sys.exit(1)

# 必要列チェック（日本語ヘッダや英語ヘッダに対応）
# 優先列名: name, lat, lon
cols = list(stores_df.columns)
print("CSV 列名:", cols)
# try common japanese headers
if {"name", "lat", "lon"}.issubset(stores_df.columns):
    name_col, lat_col, lon_col = "name", "lat", "lon"
elif {"店舗名", "緯度", "経度"}.issubset(stores_df.columns):
    name_col, lat_col, lon_col = "店舗名", "緯度", "経度"
else:
    # try fuzzy: choose first three columns as name, lat, lon
    name_col, lat_col, lon_col = cols[0], cols[1], cols[2]
    print(f"警告: 列名が標準でありません。自動割当: name={name_col}, lat={lat_col}, lon={lon_col}")

# normalize dataframe columns into expected types
stores_df = stores_df[[name_col, lat_col, lon_col]].rename(columns={name_col: "name", lat_col: "lat", lon_col: "lon"})
stores_df["lat"] = stores_df["lat"].astype(float)
stores_df["lon"] = stores_df["lon"].astype(float)
print(f"店舗件数: {len(stores_df)}")

# ---------- 1) 道路ネットワークの取得 ----------
print("1) OSMnx で道路ネットワークを取得します（前橋市全域）...")
# 取得範囲を狭めたい場合は graph_from_bbox / graph_from_point に変えてください
G = ox.graph_from_place(PLACE, network_type="drive")
print(f"   ノード数={len(G.nodes)}, エッジ数={len(G.edges)}")

# ---------- 2) 各店舗を最寄ノードにスナップ ----------
print("2) 各店舗を道路ノードにスナップ（nearest_nodes）...")
store_nodes = {}
for _, row in stores_df.iterrows():
    name = str(row["name"])
    lat, lon = float(row["lat"]), float(row["lon"])
    # ox.distance.nearest_nodes の引数順は X=lon, Y=lat
    node = ox.distance.nearest_nodes(G, X=lon, Y=lat)
    store_nodes[name] = node
print(f"   スナップ完了（{len(store_nodes)} 店舗）")

# 同一ノードに複数店舗が割り当たる可能性に備える辞書
node_to_stores = {}
for name, node in store_nodes.items():
    node_to_stores.setdefault(node, []).append(name)

# ---------- 3) multi-source Dijkstra で各ノードの最寄りソースを一度に計算 ----------
print("3) multi_source_dijkstra を実行して各ノードの最寄り店舗を一度に計算します（高速）...")
sources = list(node_to_stores.keys())  # ソースノード一覧
# multi_source_dijkstra: distances: dict(node->dist), paths: dict(node->path_list)
distances, paths = nx.multi_source_dijkstra(G, sources=sources, weight="length")
print("   multi_source_dijkstra 完了")

# node -> store_name の割当て
node_owner = {}
for node, path in paths.items():
    if not path:
        node_owner[node] = None
    else:
        src_node = path[0]
        # src_node に割り当てられた店舗名リスト（複数あり得る）
        stores_here = node_to_stores.get(src_node, [])
        node_owner[node] = stores_here[0] if stores_here else None



# ---------- 4) Folium マップ作成（HTML出力用） ----------
print("4) Folium 地図を作成して HTML に保存します...")
# 地図中心はノードの平均座標
ys = [data["y"] for _, data in G.nodes(data=True)]
xs = [data["x"] for _, data in G.nodes(data=True)]
center = (sum(ys) / len(ys), sum(xs) / len(xs))
m = folium.Map(location=center, zoom_start=13, tiles="cartodbpositron")


import random
store_names = list(store_nodes.keys())
n = max(len(store_names), 1)

if n <= 20:
    cmap = cm.get_cmap("tab20", n)
    base_colors =  [mcolors.to_hex(cmap(i)) for i in range(n)]
else:
    cmap = cm.get_cmap("hsv", n)
    base_colors = [mcolors.to_hex(cmap(i)) for i in range(n)]
    random.shuffle(base_colors)

colors = {name: base_colors[i % len(base_colors)] for i, name in enumerate(store_names)}

edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
print(" edgesの件数:", len(edges))
count_drawn = 0
for idx, row in edges.iterrows():
    try:
        u, v = idx[0], idx[1]
    except Exception:
        continue

    owner_u = node_owner.get(u)
    owner_v = node_owner.get(v)

    if owner_u is not None and owner_v is not None and owner_u == owner_v:
        coords = [(pt[1], pt[0]) for pt in row.geometry.coords]
        folium.PolyLine(
            locations=coords,
            color=colors.get(owner_u, "#888888"),
            weight=2,
            opacity=0.8
        ).add_to(m)
        count_drawn += 1
print(f" 描画したエッジ数: {count_drawn}")


# カラーマップ（店舗の数だけ色を配る）
store_names = list(store_nodes.keys())
n = max(len(store_names), 1)
cmap = cm.get_cmap("hsv", n)
colors = {name: mcolors.to_hex(cmap(i)) for i, name in enumerate(store_names)}

# edges GeoDataFrame を取得して MultiIndex に対応して描画
edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
print("   edges の件数:", len(edges))
count_drawn = 0
for idx, row in edges.iterrows():
    # idx が (u,v,key) の MultiIndex の想定
    try:
        u, v = idx[0], idx[1]
    except Exception:
        # 万が一インデックス形式が違えばスキップ
        continue
    owner_u = node_owner.get(u)
    owner_v = node_owner.get(v)
    if owner_u and owner_u == owner_v:
        # geometry.coords は (lon, lat) 順 → folium 用に (lat, lon) に変換
        coords = [(pt[1], pt[0]) for pt in row.geometry.coords]
        folium.PolyLine(locations=coords, color=colors.get(owner_u, "#888888"), weight=2, opacity=0.7).add_to(m)
        count_drawn += 1
print(f"   描画したエッジ数: {count_drawn}")

# 店舗マーカーを追加（色を合わせる）
for _, row in stores_df.iterrows():
    name = row["name"]
    folium.CircleMarker(
        location=(row["lat"], row["lon"]),
        radius=4,
        color=colors.get(name, "#000000"),
        fill=True,
        fill_opacity=0.9,
        popup=name
    ).add_to(m)

# 保存
m.save(OUT_HTML)
print(f"✅ 完了しました — 出力ファイル: {OUT_HTML}")
print("ブラウザで開いて確認してください。")


# ---------- 5) 各店舗のネットワークボロノイ領域を Shapefile に出力 ----------
import geopandas as gpd
from shapely.geometry import LineString

output_dir = "output_voronoi"
os.makedirs(output_dir, exist_ok=True)

print("5) Shapefile 出力を開始します...")

# edges はすでに ox.graph_to_gdfs() で取得済み
# node_owner と colors, store_nodes も上で定義済み

store_edges = {name: [] for name in store_nodes.keys()}

for idx, row in edges.iterrows():
    try:
        u, v = idx[0], idx[1]
    except Exception:
        continue
    owner_u = node_owner.get(u)
    owner_v = node_owner.get(v)
    if owner_u and owner_u == owner_v:
        # その店舗の領域に属するエッジを追加
        coords = [(pt[0], pt[1]) for pt in row.geometry.coords]  # (lon, lat)
        store_edges[owner_u].append(LineString(coords))

# 各店舗ごとにShapefileとして保存
for store_name, line_list in store_edges.items():
    if not line_list:
        continue
    gdf = gpd.GeoDataFrame({'store': [store_name] * len(line_list)},
                           geometry=line_list,
                           crs="EPSG:4326")
    safe_name = store_name.replace("/", "_").replace("\\", "_").replace(" ", "_")
    shp_path = os.path.join(output_dir, f"{safe_name}.shp")
    gdf.to_file(shp_path, driver="ESRI Shapefile")
    print(f"  → {store_name}: {len(line_list)} 本のエッジを保存 ({shp_path})")

print("✅ 全店舗のShapefile出力が完了しました。")
print(f"フォルダを開いてQGISにドラッグ＆ドロップしてください: {output_dir}")
