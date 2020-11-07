from django.urls import path

from . import  views

urlpatterns = [
    path('', views.index, name='listings'),
    path('<slug:slug>', views.listing, name='listing'),
    path('search/', views.search, name='search'),
    path('vendors/', views.vendors, name='vendors'),
    path('categories/', views.categories, name='categories'),
    path('categories/<slug:slug>', views.category, name='category'),

    path('vendors/<slug:slug>', views.vendor, name="vendor"),
]
 