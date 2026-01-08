import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from graph import users, movies, G

# 1. Строим матрицу пользователь–фильм
user_to_idx = {user: i for i, user in enumerate(users)}
movie_to_idx = {movie: j for j, movie in enumerate(movies)}
R = np.zeros((len(users), len(movies)), dtype=int)

for u, m in G.edges():
    if u in user_to_idx and m in movie_to_idx:
        R[user_to_idx[u], movie_to_idx[m]] = 1
    elif m in user_to_idx and u in movie_to_idx:
        R[user_to_idx[m], movie_to_idx[u]] = 1

# 2. Сходство пользователей
user_similarity = cosine_similarity(R)


# 3. Функция рекомендаций
def recommend_movies_for_user(target_user, top_k=2):
    u_idx = user_to_idx[target_user]
    recommendations = []
    for j, movie in enumerate(movies):
        if R[u_idx, j] == 1:
            continue
        users_who_rated = R[:, j] == 1
        if not np.any(users_who_rated):
            score = 0.0
        else:
            sims = user_similarity[u_idx][users_who_rated]
            total = np.sum(np.abs(sims))
            score = np.sum(sims) / total if total > 0 else 0.0
        recommendations.append((movie, score))
    return sorted(recommendations, key=lambda x: x[1], reverse=True)[:top_k]


# 4. Вывод рекомендаций
print("\n" + "=" * 50)
print("РЕКОМЕНДАЦИИ ЧЕРЕЗ КОЛЛАБОРАТИВНУЮ ФИЛЬТРАЦИЮ")
print("=" * 50)
for user in users:
    recs = recommend_movies_for_user(user, top_k=2)
    print(f"\n{user}:")
    for movie, score in recs:
        print(f"  → {movie} (сходство: {score:.3f})")
