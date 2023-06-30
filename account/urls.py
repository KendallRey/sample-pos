from django.urls import path

from . import views

urlpatterns = [
    # path('me', views.get_current_user, name="[get] user info"),
    path('register', views.UserRegister.as_view()),
    path('me', views.GetCurrentUser.as_view(), name="[get] user info"),
    path('me/update/<str:id>', views.UpdateUser.as_view(), name="[update] user info"),
    path('me/update-password/<str:id>', views.UpdateUserPassword.as_view(), name="[update - password] user info"),
]
