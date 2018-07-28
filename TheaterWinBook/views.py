

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import UserForm, LoginForm
from .models import Post


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'TheaterWinBook/post_list.html', {'posts':posts})


def index(request):
    return render(request, 'TheaterWinBook/index.html')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'TheaterWinBook/post_detail.html', {'post': post})


def winbook_insert(request):
    return render(request, 'TheaterWinBook/winbook_insert.html')


def winbook_list(request):
    return render(request, 'TheaterWinBook/winbook_list.html')


def to_winnerBros(request):
    return render(request, 'TheaterWinBook/to_winnerBros.html')


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        print('post')
        if form.is_valid():
            # 회원가입 정보를 이용하여 새로운 사용자 만들기.
            print('valid1')
            new_user = User.objects.create_user(**form.cleaned_data)
            # 회원가입을 하고 로그인을 바로 하는 것이 아니라, 로그인 페이지로 이동시키자
            # login(request, new_user)
            print('valid2')
            signup_try = 'signup_success'
            return render(request, 'TheaterWinBook/login_view.html', {'signup_try': signup_try})
        else:
            form = UserForm()
            # 검증에 실패시 form.error 에 오류 정보를 저장하여 함께 렌더링

            return render(request, 'TheaterWinBook/signup.html', {'form': form})

    else:
        print('signup_else part')
        form = UserForm()
        return render(request, 'TheaterWinBook/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            login_try = 'login_fail'
            return render(request, 'TheaterWinBook/login_view.html', {'form': form,'login_try':login_try})
    else:
        form = LoginForm()
        return render(request, 'TheaterWinBook/login_view.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


# 아이디 중복 체크를 위한 AJAX
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    print ("this is is_taken:", data)
    return JsonResponse(data)


