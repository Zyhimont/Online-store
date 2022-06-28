from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/<slug:category_slug>/', views.catalog, name='catalog'),
    path('catalog/', views.catalog, {'category_slug': None}, name='catalog'),
]
