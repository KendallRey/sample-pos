from django.urls import path

from . import views

urlpatterns = [
    # path('me', views.get_current_user, name="[get] user info"),
    path('me', views.GetCurrentUser.as_view(), name="[get] user info"),
    path('me/update/<str:id>', views.UpdateUser.as_view(), name="[update] user info"),
]
