from django.urls import path

from rec_system.views import RecommendView, PreferenceView, StatsView, PrefListView

app_name = 'rec_system'

urlpatterns = [
    path('recommend/', RecommendView.as_view(), name='recommend'),
    path('pref_list/', PrefListView.as_view(), name='pref_list'),
    path('preference/', PreferenceView.as_view(), name='preference'),
    path('stats/', StatsView.as_view(), name='stats'),
]
