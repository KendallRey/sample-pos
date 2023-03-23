from django.urls import path
from django.conf.urls import include

from . import views;

urlpatterns = [
    path('list', views.ItemList.as_view(), name="[list] - item"),
    path('create', views.ItemCreate.as_view(), name="[create] - item"),
    path('<str:id>', views.ItemUpdate.as_view(), name="[update] - item"),
    # path('<pk>', views.ItemUpdateDelete.as_view(), name="[update,delete] - item"),
]
