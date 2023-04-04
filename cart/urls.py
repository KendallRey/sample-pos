from django.urls import path

from . import views

urlpatterns = [
    path('list', views.CartList.as_view(), name="[list] - cart"),
    path('cart-items/<str:id>', views.CartItemList.as_view(), name="[cart-item-list] - cart")
]
