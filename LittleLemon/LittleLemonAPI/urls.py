from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('menu-items/', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>/', views.SingleMenuItemView.as_view()),
    path('cart/menu-items', views.CartView.as_view()),
    path('orders/', views.OrderView.as_view()),
    path('orders/<int:pk>/', views.OrderItemView.as_view()),
]
