import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

data = pd.read_csv('earthquake data.csv', nrows=5000).replace({'Country': {'\"': ''}}, regex=True)

G = nx.Graph()

for i in range(len(data)):
    for j in range(i + 1, len(data)):
        distance = haversine(data['Latitude'][i], data['Longitude'][i], data['Latitude'][j], data['Longitude'][j])
        
        if 0 < distance < 3000 and data['Country'][i] != data['Country'][j]:
            avg_magnitude = (data['Magnitude'][i] + data['Magnitude'][j]) / 2
            G.add_edge(data['Country'][i], data['Country'][j], weight=avg_magnitude)

filtered_edges = [(i, j) for i, j, weight in G.edges(data='weight') if weight > 4]

H = G.edge_subgraph(filtered_edges)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

pos = nx.spring_layout(H, k=0.30)
nx.draw_networkx_nodes(H, pos, node_size=100, node_color='skyblue', ax=ax1)
nx.draw_networkx_edges(H, pos, ax=ax1)
nx.draw_networkx_labels(H, pos, font_size=8, font_color='black', font_weight='bold', ax=ax1)
ax1.set_title('Grafo com Regiões e suas Magnitudes')

top_countries = data.groupby('Country')['Magnitude'].max().sort_values(ascending=False).head(10)
ax2.barh(top_countries.index, top_countries.values, color='orange')
ax2.set_title('Top 10 Países com Maiores Magnitudes')
ax2.invert_yaxis()

plt.tight_layout()
plt.show()
