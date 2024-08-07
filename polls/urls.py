from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("comments/", views.CommentsView.as_view(), name="comments"),

    path("comment/", views.comment, name="comment"),

    path("userData/", views.user_data, name="userData"),

    path("login/", views.LoginView.as_view(), name="login"),
    path("post_login/", views.user_login, name="user_login"),

    path("request-reset-password/", views.RequestResetPasswordView.as_view(), name="request-reset-password"),
    path("post-request-reset-password/", views.post_request_reset_password, name="post-request-reset-password"),

    path("reset-password/", views.reset_password, name="reset-password"),
    path("post-reset-password/", views.post_reset_password, name="post-reset-password"),

    path("logout/", views.logout_user, name="logout"),

    path("author/", views.AuthorView.as_view(), name="author")


]
