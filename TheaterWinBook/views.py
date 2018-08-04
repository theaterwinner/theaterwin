from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import UserForm, LoginForm, TheaterWinBookRecordForm
from .models import Post, TheaterWinBookRecord


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'TheaterWinBook/post_list.html', {'posts':posts})


def index(request):
    return render(request, 'TheaterWinBook/index.html')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'TheaterWinBook/post_detail.html', {'post': post})


@login_required(login_url='/login_view')
def winbook_calendar(request):
    return render(request, 'TheaterWinBook/winbook_calendar.html')


@login_required(login_url='/login_view')
def winbook_insert(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TheaterWinBookRecordForm(request.POST)  # PostForm으로 부터 받은 데이터를 처리하기 위한 인스턴스 생성
        if form.is_valid():  # 폼 검증 메소드
            inputForm = form.save(commit=False)  # 오브젝트를 form으로 부터 가져오지만, 실제로 DB반영은 하지 않는다.
            # 가져 온 후 데이터 처리를 ㅐㅎ도 된다.
            inputForm.user_name = request.user
            # inputForm 저장하기
            inputForm.save()
            # 저장한 후에 pk 값 가져오기
            print("this is after saving records pk :",inputForm.pk);
            # 정보를 성공적으로 입력한 후에는 방금 정리되었던
            return redirect('index')  # url의 name을 경로대신 입력한다.
        else:

            messages.error(request, "please enter right field");

    else:
        form = TheaterWinBookRecordForm()  # forms.py의 PostForm 클래스의 인스턴스
    return render(request, 'TheaterWinBook/winbook_insert.html', {'form': form})  # 템플릿 파일 경로 지정, 데이터 전달


def winbook_statistics(request):
    return render(request, 'TheaterWinBook/winbook_statistics.html')


@login_required(login_url='/login_view')
def winbook_list(request):
    login_user_name = request.user
    winbook_user_result = TheaterWinBookRecord.objects.filter(user_name=login_user_name)
    winbook_user_list = {"winbook_user_result":winbook_user_result}

    return render(request, 'TheaterWinBook/winbook_list.html',winbook_user_list)


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
    next = request.GET.get('next', '/')
    print('this is next:',next);
    # 만약 nextpage 가 /login_view/라면 index페이지로 넘기자
    if(next =='/login_view/'):
        next = '/index'
    if(next=='/' or next=='/index/'):
        auth_page = 'no'
    else:
        auth_page = 'yes'
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)


        else:
            login_try = 'login_fail'
            return render(request, 'TheaterWinBook/login_view.html', {'form': form,'login_try':login_try,'auth_page':auth_page})
    else:
        form = LoginForm()
        return render(request, 'TheaterWinBook/login_view.html', {'form': form,'auth_page':auth_page})


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


