from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Post
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'TheaterWinBook/post_list.html', {'posts':posts})


def index(request):
    return render(request, 'TheaterWinBook/index.html')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'TheaterWinBook/post_detail.html', {'post': post})


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # 회원가입 정보를 이용하여 새로운 사용자 만들기.
            new_user = User.objects.create_user(**form.cleaned_data)
            # 회원가입을 하고 로그인을 바로 하는 것이 아니라, 로그인 페이지로 이동시키자
            login(request, new_user)
            return redirect('login')
    else:
        form = UserForm()
        return render(request, 'TheaterWinBook/signup.html', {'form': form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'TheaterWinBook/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')

