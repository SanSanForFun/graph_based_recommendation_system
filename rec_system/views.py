from rest_framework.response import Response
from rest_framework.views import APIView
from .graph import add_preference, colab_filter, get_stats, knn, personal_page_rank


class RecommendView(APIView):
    def get(self, request):
        user = request.query_params.get('user')
        method = request.query_params.get('method', 'cf')  # cf, knn, ppr
        k = int(request.query_params.get('k', 3))

        if not user:
            return Response({"error": "user required"}, status=400)

        if method == 'cf':
            recs = colab_filter(user, k)
        elif method == 'knn':
            recs = knn(user, k_neighbors=min(k, 3), top_n=k)
        elif method == 'ppr':
            recs = personal_page_rank(user, k)
        else:
            return Response({"error": "method must be 'cf', 'knn' or 'ppr'"}, status=400)

        return Response({"user": user, "recommendations": recs})


class PreferenceView(APIView):
    def post(self, request):
        user = request.data.get('user')
        item = request.data.get('item')
        if not user or not item:
            return Response({"error": "user and item required"}, status=400)
        add_preference(user, item)
        return Response({"status": "success"})


class StatsView(APIView):
    def get(self, request):
        return Response(get_stats())
