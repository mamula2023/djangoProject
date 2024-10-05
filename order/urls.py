from django.urls import path

from store.urls import urlpatterns
from . import views

urlpatterns = [
    path('<int:order_id>', views.index, name='index'),
    path('history', views.history, name='history'),
]
