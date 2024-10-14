from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('category/', views.category, name='category')

]
