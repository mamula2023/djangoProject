from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('category/', views.category, name='category'),

    path('category/<int:category_id>/products', views.category_products, name='category_products'),

]
