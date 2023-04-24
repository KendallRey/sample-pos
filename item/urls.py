from django.urls import path

from . import views;

urlpatterns = [
    path('list', views.ItemList.as_view(), name="[list] - item"),
    path('create', views.ItemCreate.as_view(), name="[create] - item"),
    path('retrieve/<str:id>', views.ItemRetrieve.as_view(), name="[retrieve] - item"),
    path('update/<str:id>', views.ItemUpdate.as_view(), name="[update] - item"),
    path('delete/<str:id>', views.ItemDelete.as_view(), name="[delete] - item"),

    path('category/list', views.ItemCategoryList.as_view(), name="[category-list] - item"),
    path('category/create', views.ItemCreate.as_view(), name="[category-create] - item"),
    path('category/retrieve/<str:id>', views.ItemRetrieve.as_view(), name="[category-retrieve] - item"),
    path('category/update/<str:id>', views.ItemUpdate.as_view(), name="[category-update] - item"),
    path('category/delete/<str:id>', views.ItemDelete.as_view(), name="[category-delete] - item"),

    path('image/list', views.ItemImageList.as_view(), name="[image-list] - item"),
    path('image/create', views.ItemImageCreate.as_view(), name="[image-create] - item"),
    path('image/update/<str:id>', views.ItemImageUpdate.as_view(), name="[image-update] - item"),
]
