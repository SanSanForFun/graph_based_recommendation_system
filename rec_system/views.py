from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from rec_system.models import Interaction
from .graph import add_preference, colab_filter, get_stats, knn, personal_page_rank
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


@method_decorator(cache_page(60 * 15), name='dispatch')
class RecommendView(TemplateView):
    """ Рекомендации для пользователя """
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


@method_decorator(cache_page(60 * 15), name='dispatch')
class PreferenceView(View):
    """ Добавление предпочтений """
    template_name = 'rec_system/preference.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.POST.get('user', '').strip()
        movie_input = request.POST.get('movie', '').strip()

        if not user or not movie_input:
            messages.error(request, "Имя и хотя бы один фильм обязательны.")
            return render(request, self.template_name)

        # Разделяем по запятой
        movies_list = [m.strip() for m in movie_input.split(',') if m.strip()]

        try:
            # Сохраняем предпочтения
            add_preference(user, movies_list)

            # Генерируем рекомендации
            recommendations = colab_filter(user, k=5)  # или top_k=5, если не меняли сигнатуру

        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")
            recommendations = []

        return render(request, self.template_name, {
            'user': user,
            'recommendations': recommendations,
        })


class PrefListView(View):
    """ Список фильмов пользователя """
    template_name = 'rec_system/pref_list.html'

    def get(self, request):
        user = request.GET.get('user', '').strip()

        if not user:
            return render(request, self.template_name, {
                'error': 'Параметр "user" обязателен'
            })

        # Получаем фильмы из БД
        movies = Interaction.objects.filter(user=user).values_list('movie', flat=True).distinct()
        movies_list = list(movies)

        # Передаём в шаблон
        return render(request, self.template_name, {
            'user': user,
            'movies': movies_list,
        })


class StatsView(TemplateView):
    """ Отображение статистики системы """
    template_name = 'rec_system/statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = get_stats()
        return context
