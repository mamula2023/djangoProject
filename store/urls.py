from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('item/<int:item_id>/', views.item, name='item'),
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products')
]
