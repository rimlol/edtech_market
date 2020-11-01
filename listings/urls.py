from django.urls import path

from . import  views

urlpatterns = [
    path('', views.index, name='listings'),
    path('<slug:slug>', views.listing, name='listing'),
    path('search/', views.search, name='search'),
    path('vendors/', views.vendors, name='vendors'),
    path('vendors/<slug:slug>', views.vendor, name="vendor"),
]
 