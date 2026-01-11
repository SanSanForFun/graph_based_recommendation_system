import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Рисуем граф
G = nx.Graph()

# Определяем элементы графа
users = ['Вася', 'Петя', 'Маша']
movies = ['Такси', 'Красная жара', 'Терминатор', 'Хоббит', 'Сумерки']

# Добавляем вершины графа
for user in users:
    G.add_node(user)

for movie in movies:
    G.add_node(movie)

# Добавляем ребра-отношения
G.add_edge('Вася', 'Терминатор')
G.add_edge('Вася', 'Хоббит')
G.add_edge('Вася', 'Такси')
G.add_edge('Петя', 'Красная жара')
G.add_edge('Петя', 'Терминатор')
G.add_edge('Петя', 'Такси')
G.add_edge('Маша', 'Сумерки')
G.add_edge('Маша', 'Такси')
G.add_edge('Маша', 'Хоббит')


def add_preference(user: str, item: str):
    """Добавить взаимодействие пользователя с элементом"""
    G.add_node(user, type='user')
    G.add_node(item, type='movie')
    G.add_edge(user, item)
    users.add(user)
    movies.add(item)


def personal_page_rank(user, top_k=2):
    """ Функция для определения важности каждого узла (Page Rank) """
    # Вычисляем PageRank
    pers = {node: 1.0 if node == user else 0.0 for node in G.nodes}
    ppr = nx.pagerank(G, personalization=pers, alpha=0.85)
    # Только фильмы, которых пользователь ещё не смотрел
    watched = set(m for u, m in G.edges(user))
    movie_scores = [(m, ppr[m]) for m in movies if m not in watched]
    return sorted(movie_scores, key=lambda x: x[1], reverse=True)[:top_k]


# Пример для пользователя Вася
print("\nPPR-рекомендации для Васи:")
for movie, score in personal_page_rank('Вася'):
    print(f"  {movie}: {score:.4f}")


def matrix():
    """ Строим матрицу пользователь-фильм """
    user_to_idx = {user: i for i, user in enumerate(users)}
    movie_to_idx = {movie: j for j, movie in enumerate(movies)}
    R = np.zeros((len(users), len(movies)), dtype=int)

    for u, m in G.edges():
        if u in user_to_idx and m in movie_to_idx:
            R[user_to_idx[u], movie_to_idx[m]] = 1
        elif m in user_to_idx and u in movie_to_idx:
            R[user_to_idx[m], movie_to_idx[u]] = 1

    return R, user_to_idx, movie_to_idx


def colab_filter(user, top_k=2):
    """ Рекомендации на основе алгоритма коллаборативной фильтрации """
    if user not in users:
        return []

    R, user_to_idx, movie_to_idx = matrix()
    if R is None:
        return []

    movie_list = sorted(movies)
    u_idx = user_to_idx[user]
    user_similarity = cosine_similarity(R)

    recommendations = []
    for j, movie in enumerate(movie_list):
        if R[u_idx, j] == 1:  # уже просмотрено
            continue
        users_who_rated = R[:, j] == 1
        if not np.any(users_who_rated):
            score = 0.0
        else:
            sims = user_similarity[u_idx][users_who_rated]
            total = np.sum(np.abs(sims))
            score = np.sum(sims) / total if total > 0 else 0.0
        recommendations.append((movie, score))

    recommendations.sort(key=lambda x: x[1], reverse=True)
    return [movie for movie, _ in recommendations[:top_k]]


def knn(user: str, k_neighbors: int = 2, top_n: int = 3):
    """ Рекомендации через k-ближайших соседей (k-NN) """
    if user not in users:
        return []

    R, user_to_idx, movie_to_idx = matrix()
    if R is None:
        return []

    movie_list = sorted(movies)
    u_idx = user_to_idx[user]
    user_similarity = cosine_similarity(R)

    # Найти k ближайших соседей
    similarities = user_similarity[u_idx].copy()
    similarities[u_idx] = -1  # исключить себя
    nearest_indices = np.argsort(similarities)[-k_neighbors:][::-1]

    # Агрегировать оценки соседей
    scores = np.sum(R[nearest_indices], axis=0)

    # Исключить уже просмотренные
    scores[R[u_idx] == 1] = -1

    # Топ-N
    top_indices = np.argsort(scores)[-top_n:][::-1]
    return [movie_list[i] for i in top_indices if scores[i] > 0]


def get_stats():
    """Получить статистику по системе"""
    if not movies:
        most_popular = None
    else:
        most_popular = max(movies, key=lambda m: G.degree(m))
    return {
        "total_users": len(users),
        "total_items": len(movies),
        "interactions_count": G.number_of_edges(),
        "most_popular_item": most_popular
    }
