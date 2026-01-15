from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .graph import add_preference, colab_filter, get_stats, knn, personal_page_rank
from django.contrib import messages


class RecommendView(TemplateView):
    template_name = 'rec_system/recommendation.html'

    def get(self, request, *args, **kwargs):
        user = request.GET.get('user')
        method = request.GET.get('method', 'cf')
        k = int(request.GET.get('k', 3))

        context = {'user': user}

        if not user:
            context['error'] = 'Параметр "user" обязателен'
            return render(request, self.template_name, context)

        try:
            if method == 'cf':
                recs = colab_filter(user, k)
            elif method == 'knn':
                recs = knn(user, k_neighbors=min(k, 3), top_n=k)
            elif method == 'ppr':
                recs = personal_page_rank(user, k)
            else:
                context['error'] = 'Метод должен быть: cf, knn или ppr'
                return render(request, self.template_name, context)
        except Exception as e:
            context['error'] = f'Ошибка при генерации рекомендаций: {str(e)}'
            return render(request, self.template_name, context)

        # Передаём рекомендации в шаблон
        context['recommendations'] = recs
        return render(request, self.template_name, context)


class PreferenceView(View):
    template_name = 'rec_system/preference.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.POST.get('user')
        movie = request.POST.get('movie')
        if not user or not movie:
            messages.error(request, "Имя пользователя и фильм обязательны.")
            return render(request, self.template_name, status=400)

        add_preference(user, movie)
        messages.success(request, "Предпочтение сохранено!")
        return redirect('preference')


class StatsView(TemplateView):
    template_name = 'rec_system/statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = get_stats()
        return context
