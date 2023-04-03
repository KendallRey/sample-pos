from django.urls import path

from . import views

urlpatterns = [
    path('list', views.CartList.as_view(), name="[list] - cart")
]
