from django.urls import path, include, re_path
from weatherservice import views

app_name='weatherservice'

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('ping/', views.ping, name='ping'),
    path('forecast/', views.forecast, name='forecast'),
    path('forecast/<city>/', views.HomeView.as_view(), name='home'),
    re_path(r'^forecast/(?P<city>\w+)/(?P<temp_unit>\w+)/$', views.HomeView.as_view(), name='temp_unit'),
]

