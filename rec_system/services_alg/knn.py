import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from rec_system.graph import users, movies, G

# Строим матрицу пользователь–фильм
user_to_idx = {u: i for i, u in enumerate(users)}
movie_to_idx = {m: j for j, m in enumerate(movies)}

R = np.zeros((len(users), len(movies)), dtype=int)
for u, m in G.edges():
    if u in user_to_idx and m in movie_to_idx:
        R[user_to_idx[u], movie_to_idx[m]] = 1
    elif m in user_to_idx and u in movie_to_idx:
        R[user_to_idx[m], movie_to_idx[u]] = 1

# Вычислим попарное сходство (косинус)
user_sim = cosine_similarity(R)


# Функция: найти k ближайших пользователей
def find_k_nearest_users(target_user, k=2):
    u_idx = user_to_idx[target_user]
    # Исключаем самого себя (сходство = 1.0)
    similarities = user_sim[u_idx].copy()
    similarities[u_idx] = -1  # чтобы не выбрать себя
    nearest_indices = np.argsort(similarities)[-k:][::-1]  # топ-k
    return [(users[i], similarities[i]) for i in nearest_indices]


# Пример: найти 2 ближайших к первому пользователю
target = users[0]
k = 2
nearest = find_k_nearest_users(target, k)
print(f"\n{k}-ближайших соседей для {target}:")
for user, sim in nearest:
    print(f"  {user} (сходство: {sim:.3f})")


# Рекомендация на основе k-NN
def knn_recommend(target_user, k=2, top_n=2):
    neighbors = find_k_nearest_users(target_user, k)
    neighbor_indices = [user_to_idx[u] for u, _ in neighbors]

    # Суммируем оценки соседей
    scores = np.sum(R[neighbor_indices], axis=0)

    # Исключаем уже просмотренные
    target_idx = user_to_idx[target_user]
    scores[R[target_idx] == 1] = -1  # помечаем как "уже известные"

    # Топ-N рекомендаций
    top_movie_indices = np.argsort(scores)[-top_n:][::-1]
    return [(movies[i], scores[i]) for i in top_movie_indices if scores[i] > 0]


# Пример рекомендации
recs = knn_recommend(users[0], k=2, top_n=2)
print(f"\nРекомендации для {users[0]} через k-NN:")
for movie, score in recs:
    print(f"  {movie} (поддержано {int(score)} соседями)")
