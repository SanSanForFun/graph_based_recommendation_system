import networkx as nx

# import matplotlib.pyplot as plt

# Рисуем граф
G = nx.DiGraph()

# Определяем элементы графа
users = ['Вася', 'Петя', 'Маша']
movies = ['Такси', 'Красная жара', 'Терминатор', 'Хоббит', 'Сумерки']

# Добавляем вершины графа
for user in users:
    G.add_node(user)

for movie in movies:
    G.add_node(movie)

# Добавляем ребра
G.add_edge('Вася', 'Терминатор')
G.add_edge('Вася', 'Хоббит')
G.add_edge('Вася', 'Такси')
G.add_edge('Петя', 'Красная жара')
G.add_edge('Петя', 'Терминатор')
G.add_edge('Петя', 'Такси')
G.add_edge('Маша', 'Сумерки')
G.add_edge('Маша', 'Такси')
G.add_edge('Маша', 'Хоббит')


# Если убрать коммиты, то можно увидеть изначальный граф


# Для корректного отображения графа разделим пользователей и фильмы на две колонки
# pos = {}
# Пользователи — слева
# for i, user in enumerate(users):
#     pos[user] = (0, len(users) - i)
# Фильмы — справа
# for i, movie in enumerate(movies):
#     pos[movie] = (1, len(movies) - i)

# plt.figure(figsize=(10, 6))
# nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=5000,
#         font_size=8, font_weight='bold', edge_color='gray')
# plt.title('Граф предпочтений: пользователи - элементы')
# plt.show()
