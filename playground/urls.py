from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('add/', views.say_hello),
    path('people/', views.show_people),
    path('', views.home, name='home'),
]