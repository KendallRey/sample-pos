from django.urls import path

from . import views

urlpatterns = [
    path('list', views.OrderItemList.as_view(), name="[list] - order items"),
    path('list/<str:id>', views.OrderItemList.as_view(), name="[list] - order items from shop"),
    path('create', views.OrderItemCreate.as_view(), name="[create] - order item"),
    path('retrieve/<str:id>', views.OrderItemRetrieve.as_view(), name="[retrieve] - order item"),
    path('update/<str:id>', views.OrderItemUpdate.as_view(), name="[update] - order item"),
    path('delete/<str:id>', views.OrderItemDelete.as_view(), name="[delete] - order item"),
]