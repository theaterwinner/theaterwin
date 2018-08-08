from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import UserForm, LoginForm, TheaterWinBookRecordForm
from .models import Post, TheaterWinBookRecord
from django.contrib import messages
from django.contrib.messages import get_messages
import json


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'TheaterWinBook/post_list.html', {'posts': posts})


def error_404(request):
    return render(request, 'TheaterWinBook/error_404.html')


def error_wronguser(request):
    return render(request, 'TheaterWinBook/error_wronguser.html')


def index(request):
    return render(request, 'TheaterWinBook/index.html')


def index_video_test(request):
    return render(request, 'TheaterWinBook/index_video_test.html')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'TheaterWinBook/post_detail.html', {'post': post})


@login_required(login_url='/login_view')
def winbook_calendar(request):
    return render(request, 'TheaterWinBook/winbook_calendar.html')


@login_required(login_url='/login_view')
def winbook_modify(request):
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
            print("this is after modifying records pk :", inputForm.pk)
            modify_winbook_pk = inputForm.pk
            messages.success(request, 'modify_success', extra_tags=modify_winbook_pk)
            # 정보를 성공적으로 입력한 후에는, 메세지에 방금 입력된 pk값을 담아서 보내기
            return redirect('winbook_list')
        else:
            messages.error(request, "please enter right field")
    else:
        record_pk = request.GET.get("record_pk", "")
        # 받은 pk로 글의 user를 확인한다.
        login_user = request.user
        target_record = TheaterWinBookRecord.objects.get(pk=record_pk)
        # 글을 쓴 user와 로그인된 user가 일치하는지 확인
        if (target_record.user_name == login_user):
            #   정상적으로 modify로 이동시켜준다.
            form = TheaterWinBookRecordForm(instance=target_record)  # forms.py의 PostForm 클래스의 인스턴스
            return render(request, 'TheaterWinBook/winbook_modify.html', {'form': form})
        else:
            #  그렇지 않으면 리스트로 이동시켜 준다.
            return render(request, 'TheaterWinBook/error_wronguser.html')


@login_required(login_url='/login_view')
def list_usercheck(request):
    print("this is user_check");
    # request parameter 로 winbook.pk를 받아온다.
    record_pk = request.POST.get("record_pk", "")
    # 받은 pk로 글의 user를 확인한다.
    login_user = request.user
    target_record = TheaterWinBookRecord.objects.get(pk=record_pk)
    print(target_record.user_name)
    print(request.user)
    # 글을 쓴 user와 로그인된 user가 일치하는지 확인
    usercheck_success = "fail"
    if (target_record.user_name == login_user):
        # pk번호를 기준으로 삭제를 하자.
        usercheck_success = "success";
    else:
        usercheck_success = "fail";

    return HttpResponse(json.dumps({'usercheck_success': usercheck_success}), content_type="application/json")


@login_required(login_url='/login_view')
def list_delete(request):
    # request parameter 로 winbook.pk를 받아온다.
    record_pk = request.POST.get("record_pk", "")
    # 받은 pk로 글의 user를 확인한다.
    login_user = request.user
    target_record = TheaterWinBookRecord.objects.get(pk=record_pk)
    # 글을 쓴 user와 로그인된 user가 일치하는지 확인
    delete_success = "fail"
    if (target_record.user_name == login_user):
        print('this is login user');
        # pk번호를 기준으로 삭제를 하자.
        target_record.delete()
        delete_success = "success";

    else:
        print("this is not equal login user")

    return HttpResponse(json.dumps({'delete_success': delete_success}), content_type="application/json")

    # 일치시에만 삭제 시작하고,

    # else 일치하지 않으면, 잘못된 접근 및 로그아웃 화면으로 넘기자.


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
            print("this is after saving records pk :", inputForm.pk);
            new_winbook_pk = inputForm.pk
            messages.success(request, 'insert_success', extra_tags=new_winbook_pk)
            # 정보를 성공적으로 입력한 후에는, 메세지에 방금 입력된 pk값을 담아서 보내기
            return redirect('winbook_list')
        else:

            messages.error(request, "please enter right field");

    else:
        form = TheaterWinBookRecordForm()  # forms.py의 PostForm 클래스의 인스턴스
    return render(request, 'TheaterWinBook/winbook_insert.html', {'form': form})  # 템플릿 파일 경로 지정, 데이터 전달


@login_required(login_url='/login_view')
def winbook_statistics(request):
    # 로그인된 user를 확인하고
    login_user_name = request.user
    winbook_user_result = TheaterWinBookRecord.objects.filter(user_name=login_user_name).order_by('-writing_date',
                                                                                                  '-pk')

    # 전체 통계 확인하기, 지금까지 순수익 구해보기...

    return render(request, 'TheaterWinBook/winbook_statistics.html')


@login_required(login_url='/login_view')
def winbook_list(request):
    # 신규 글 number를 메세지로 받아오기
    storage = get_messages(request)
    # 만약에 new_winbook_pk 의 디폴트 값을 설정하자..
    new_winbook_pk = 0
    new_winbook_check = 'n'
    for message in storage:
        print(message)
        # 메세지 중에서, insert_success 메세지가 있으면, extra tag에서 데이터를 가져온다.
        if str(message) == "insert_success":
            new_winbook_pk = message.extra_tags
            # 개인적으로 check 컨텍스트도 넘겨주자..
            new_winbook_check = 'y'
        else:
            print("메세지 도달 실패")

        # 로그인된 user를 확인하고
    login_user_name = request.user
    winbook_user_result = TheaterWinBookRecord.objects.filter(user_name=login_user_name).order_by('-writing_date',
                                                                                                  '-pk')

    # 현재까지 순수익 구하기.



    return render(request, 'TheaterWinBook/winbook_list.html',
                  {"winbook_user_result": winbook_user_result, "new_winbook_pk": new_winbook_pk,
                   'new_winbook_check': new_winbook_check})


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
            messages.success(request, "회원가입 완료! 가입하신 정보로 로그인해주세요!")
            return redirect('login_view')
            # signup_try = 'signup_success'
            # return render(request, 'TheaterWinBook/login_view.html', {'signup_try': signup_try})
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
    print('this is next:', next);
    # 만약 nextpage 가 /login_view/라면 index페이지로 넘기자
    if (next == '/login_view/'):
        next = '/index'
    if (next == '/' or next == '/index/'):
        auth_page = 'no'
    else:
        auth_page = 'yes'
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)


        else:
            login_try = 'login_fail'
            return render(request, 'TheaterWinBook/login_view.html',
                          {'form': form, 'login_try': login_try, 'auth_page': auth_page})
    else:
        form = LoginForm()
        return render(request, 'TheaterWinBook/login_view.html', {'form': form, 'auth_page': auth_page})


def logout_view(request):
    logout(request)
    return redirect('index')


# 아이디 중복 체크를 위한 AJAX
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    print("this is is_taken:", data)
    return JsonResponse(data)
