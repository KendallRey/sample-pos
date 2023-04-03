from django.urls import path
from django.conf.urls import include

from . import views;

urlpatterns = [
    path('list', views.ShopList.as_view(), name="[list] - item"),
    path('create', views.ShopCreate.as_view(), name="[create] - item"),
    path('retrieve', views.ShopRetrieve.as_view(), name="[retrieve] - item"),
    path('update/<str:id>', views.ShopUpdate.as_view(), name="[update] - item"),
    path('delete/<str:id>', views.ShopDelete.as_view(), name="[delete] - item"),

    # path('category/list', views.ShopCategoryList.as_view(), name="[category-list] - item"),
    # path('category/create', views.ShopCreate.as_view(), name="[category-create] - item"),
    # path('category/retrieve/<str:id>', views.ShopRetrieve.as_view(), name="[category-retrieve] - item"),
    # path('category/update/<str:id>', views.ShopUpdate.as_view(), name="[category-update] - item"),
    # path('category/delete/<str:id>', views.ShopDelete.as_view(), name="[category-delete] - item"),
]
