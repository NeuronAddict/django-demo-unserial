import base64
import pickle

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpRequest, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from polls.models import Comment
from polls.user_data import UserData


class IndexView(generic.ListView):
    template_name = "polls/comments.html"
    context_object_name = "comments_list"

    def get_queryset(self):
        """
            Return the last five published questions (not including those set to be
            published in the future).
            """
        return Comment.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class CommentsView(generic.ListView):
    template_name = "polls/comments.html"
    context_object_name = "comments_list"

    def get_queryset(self):
        return Comment.objects.order_by("-pub_date")


def comment(request: HttpRequest):

    if not request.user.is_authenticated:
        return HttpResponseForbidden("Non authenticated")

    message = request.POST['message']
    comment_text = Comment(comment_text=message, author=request.user, pub_date=timezone.now())
    comment_text.save()

    return redirect(reverse("polls:comments"))


def user_data(request: HttpRequest):

    if "data" not in request.COOKIES:
        response = HttpResponse("Setting a cookie")
        user_data = UserData(name='undefined', age=0, gender=None)
        encoded_data = base64.b64encode(pickle.dumps(user_data)).decode()

        response.set_cookie('data', f'{encoded_data}', max_age=3600)
        return response

    cookie_data = request.COOKIES['data'].split('.')
    decoded_data = base64.b64decode(cookie_data[0])

    data: UserData = pickle.loads(decoded_data)

    return render(request, "polls/user-data.html", {'data': data})


class LoginView(generic.TemplateView):

    template_name = "polls/login.html"


def user_login(request: HttpRequest):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse("polls:index"))
    else:
        return redirect(reverse("polls:login"))


def logout_user(request: HttpRequest):
    logout(request)
    return redirect(reverse("polls:index"))


def post_request_reset_password(request: HttpRequest):
    prg = PasswordResetTokenGenerator()
    username = request.POST["username"]
    token = prg.make_token(User.objects.get(username=username))
    print(f'send reset password to http://127.0.0.1:8000/reset-password/?username={username}&token=' + token)
    return redirect(reverse("polls:login"))


def reset_password(request: HttpRequest):
    prg = PasswordResetTokenGenerator()
    token = request.GET["token"]
    username = request.GET["username"]
    if prg.check_token(User.objects.get(username=username), token):
        return render(request, 'polls/change-password-form.html',
                      context={'token': token, 'username': username})
    else:
        return redirect("polls:index")


def post_reset_password(request):
    prg = PasswordResetTokenGenerator()

    token = request.POST["token"]
    username = request.POST["username"]

    if prg.check_token(User.objects.get(username=username), token):
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password != confirm_password:
            return render(request, 'polls/change-password-form.html', context={'error_massage': 'Passwords do not match'})
        else:
            user = User.objects.get(username=username)
            user.password = make_password(password)
            user.save()
            print(f'password changed for user {username}')
            return redirect(reverse("polls:login"))
    else:
        return redirect("polls:index")


class RequestResetPasswordView(generic.TemplateView):

    template_name = 'polls/request-reset-form.html'


class AuthorView(generic.TemplateView):

    template_name = "polls/author.html"


