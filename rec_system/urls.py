from django.urls import path

from rec_system.views import RecommendView, PreferenceView, StatsView

app_name = 'rec_system'

urlpatterns = [
    path('recommend/', RecommendView.as_view(), name='recommend'),
    path('preference/', PreferenceView.as_view(), name='preference'),
    path('stats/', StatsView.as_view(), name='stats'),
]
