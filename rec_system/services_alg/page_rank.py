import networkx as nx
import matplotlib.pyplot as plt
from rec_system.graph import G, users, movies

# Вычисляем PageRank
pagerank = nx.pagerank(G, alpha=0.85)  # alpha — коэффициент затухания (по умолчанию 0.85)

# Выводим результаты
print("PageRank каждого узла:")
for node, score in sorted(pagerank.items(), key=lambda x: x[1], reverse=True):
    print(f"{node:15} : {score:.4f}")

# Визуализация с размером узлов по PageRank
plt.figure(figsize=(10, 6))
pos = {}
# Пользователи — слева
for i, user in enumerate(users):
    pos[user] = (0, len(users) - i)
# Фильмы — справа
for i, movie in enumerate(movies):
    pos[movie] = (1, len(movies) - i)

# Размеры узлов пропорциональны PageRank
scores = [pagerank[node] for node in G.nodes()]
t_values = [(s - min(scores)) / (max(scores) - min(scores)) if max(scores) != min(scores) else 0 for s in scores]
node_sizes = [1000 + (t ** 2) * 2700 for t in t_values]

# Пользователи — синие, элементы — оранжевые
node_colors = ['lightblue' if node in users else 'lightcoral' for node in G.nodes()]

nx.draw(
    G, pos,
    with_labels=True,
    node_size=node_sizes,
    node_color=node_colors,
    font_size=8,
    font_weight='bold',
    edge_color='gray'
)

plt.show()
