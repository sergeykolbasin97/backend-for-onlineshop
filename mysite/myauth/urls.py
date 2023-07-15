from django.contrib.auth.views import LoginView
from django.urls import path
from .views import (
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    MyLogOutView,
    AboutMeView,
    AboutMeUpdateView,
    UserListView,
    HelloView,
    RegisterView)

app_name = "myauth"

urlpatterns = [
    path("hi/", HelloView.as_view(), name="hello"),
    path("login/", LoginView.as_view(template_name='myauth/login.html', redirect_authenticated_user=True), name="login"),
    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),
    path("session/set/", set_session_view, name="session-set"),
    path("session/get/", get_session_view, name="session-get"),
    path("logout/", MyLogOutView.as_view(), name="logout"),
    path("users/", UserListView.as_view(), name="users_list"),
    path("about-me/<int:pk>/", AboutMeView.as_view(), name="about-me"),
    path("about-me/<int:pk>/update", AboutMeUpdateView.as_view(), name="about-me_update"),
    path("register/", RegisterView.as_view(), name="register"),

]
