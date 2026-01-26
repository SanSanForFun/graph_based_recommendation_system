from django.test import TestCase, RequestFactory
from django.urls import reverse
from unittest.mock import patch
from rec_system.views import RecommendView
from rec_system.models import Interaction


class RecommendViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        Interaction.objects.create(user='Вася', movie='Терминатор')
        Interaction.objects.create(user='Вася', movie='Хоббит')
        Interaction.objects.create(user='Петя', movie='Терминатор')

    @patch('rec_system.views.colab_filter')
    def test_cf_method_success(self, mock_cf):
        """ Метод cf работает корректно"""
        mock_cf.return_value = ['Фильм1', 'Фильм2']
        request = self.factory.get('/recommend/', {'user': 'Вася', 'method': 'cf', 'k': '2'})
        response = RecommendView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Фильм1')
        self.assertContains(response, 'Фильм2')
        mock_cf.assert_called_once_with('Вася', 2)

    @patch('rec_system.views.knn')
    def test_knn_method_success(self, mock_knn):
        """ Метод knn работает корректно"""
        mock_knn.return_value = ['Фильм3', 'Фильм4']
        request = self.factory.get('/recommend/', {'user': 'Вася', 'method': 'knn', 'k': '2'})
        response = RecommendView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Фильм3')
        mock_knn.assert_called_once_with('Вася', k_neighbors=2, top_n=2)

    @patch('rec_system.views.personal_page_rank')
    def test_ppr_method_success(self, mock_ppr):
        """ Метод ppr работает корректно """
        mock_ppr.return_value = ['Фильм5', 'Фильм6']  # ← список строк
        request = self.factory.get('/recommend/', {'user': 'Вася', 'method': 'ppr', 'k': '2'})
        response = RecommendView.as_view()(request)
        self.assertContains(response, 'Фильм5')
        mock_ppr.assert_called_once_with('Вася', 2)


class PrefListViewTest(TestCase):
    def setUp(self):
        Interaction.objects.create(user='Вася', movie='Терминатор')
        Interaction.objects.create(user='Вася', movie='Хоббит')
        Interaction.objects.create(user='Петя', movie='Сумерки')

    def test_missing_user_parameter(self):
        """ Отсутствует параметр user """
        response = self.client.get(reverse('rec_system:pref_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Параметр "user" обязателен')

    def test_user_with_movies(self):
        """ Пользователь с фильмами """
        response = self.client.get('/pref_list/?user=Вася')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Терминатор')
        self.assertContains(response, 'Хоббит')
        self.assertNotContains(response, 'Сумерки')  # фильм другого пользователя


class StatsViewTest(TestCase):
    @patch('rec_system.views.get_stats')
    def test_stats_view_renders_correctly(self, mock_get_stats):
        """ Отображение статистики"""
        mock_get_stats.return_value = {
            'total_users': 100,
            'total_movies': 50,
            'interactions_count': 200,
            'most_popular_movie': 'Интерстеллар'
        }

        response = self.client.get(reverse('rec_system:stats'))

        # Проверка контекста
        self.assertIn('stats', response.context)
        stats = response.context['stats']
        self.assertEqual(stats['total_users'], 100)
        self.assertEqual(stats['most_popular_movie'], 'Интерстеллар')

        # Проверка HTML (опционально)
        self.assertContains(response, 'Интерстеллар')
        self.assertContains(response, '100')
