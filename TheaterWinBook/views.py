from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models.functions import Lower
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.encoding import smart_text

from .forms import UserForm, LoginForm, TheaterWinBookRecordForm, TheaterWinQuestionForm
from .models import Post, TheaterWinBookRecord, TheaterWinQuestion, TheaterWinQuestionInfo, TheaterWinQuestionReply, Full_Chatting_Message, TheaterWinBookRecordInfo, TheaterWinBookRecordReply
from django.contrib import messages
from django.contrib.messages import get_messages
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F
from django.db.models import Max, Min
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
import traceback
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'TheaterWinBook/post_list.html', {'posts': posts})


def error_404(request):
    return render(request, 'TheaterWinBook/error_404.html')


def bower_test(request):
    return render(request, 'TheaterWinBook/bower_test.html')


def calendar_test(request):
    return render(request, 'TheaterWinBook/calendar_test.html')


def error_wronguser(request):
    return render(request, 'TheaterWinBook/error_wronguser.html')


# is_authenticated 역할이 안되기 때문에 (필드로 변경되었기 대문에), 해당 메소드를 넣어서 wrapper method 로 사용.
def is_authenticated(user):
    if callable(user.is_authenticated):
        return user.is_authenticated()
    return user.is_authenticated


def index(request):
    if is_authenticated(request.user):
        return redirect('winbook_insert')
    else:
        return render(request, 'TheaterWinBook/index.html')


def index_real(request):
    return render(request, 'TheaterWinBook/index.html')


def index_video_test(request):
    return render(request, 'TheaterWinBook/index_video_test.html')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'TheaterWinBook/post_detail.html', {'post': post})


@login_required(login_url='/login_view')
def winbook_calendar(request):
    # 로그인된 user를 확인하고
    login_user_name = request.user
    winbook_user_result = TheaterWinBookRecord.objects.filter(user_name=login_user_name).order_by('buy_date',
                                                                                                  '-pk')
    winbook_user_result_json = serializers.serialize('json', winbook_user_result)
    # winbook_user_result_json =JsonResponse({"models_to_return": list(winbook_user_result)})
    # print(winbook_user_result)
    # winbook_user_result_json = json.dumps(list(winbook_user_result), ensure_ascii=False, default=str)
    print("this is json:" + winbook_user_result_json)
    return render(request, 'TheaterWinBook/winbook_calendar.html',
                  {"winbook_user_result_json": winbook_user_result_json})


@login_required(login_url='/login_view')
def winbook_modify(request):
    record_pk = request.GET.get("record_pk", "")
    # 받은 pk로 글의 user를 확인한다.
    login_user = request.user
    target_record = TheaterWinBookRecord.objects.get(pk=record_pk)
    # 글을 쓴 user와 로그인된 user가 일치하는지 확인
    if target_record.user_name == login_user:
        if request.method == "POST":
            # create a form instance and populate it with data from the request:
            record_pk = request.POST.get("record_pk", "")
            target_modify_record = TheaterWinBookRecord.objects.get(pk=record_pk)
            form = TheaterWinBookRecordForm(request.POST,
                                            instance=target_modify_record)  # PostForm으로 부터 받은 데이터를 처리하기 위한 인스턴스 생성
            if form.is_valid():  # 폼 검증 메소드
                inputForm = form.save(commit=False)  # 오브젝트를 form으로 부터 가져오지만, 실제로 DB반영은 하지 않는다.
                # 가져 온 후 데이터 처리를 ㅐㅎ도 된다.
                inputForm.user_name = request.user
                # inputForm 저장하기
                inputForm.save()
                # 저장한 후에 pk 값 가져오기
                print("this is after modifying records pk :", inputForm.pk)
                modify_winbook_pk = inputForm.pk
                # 정보를 성공적으로 입력한 후에는, 메세지에 방금 입력된 pk값을 담아서 보내기
                return redirect('winbook_detail', record_pk=modify_winbook_pk)
            else:
                messages.error(request, "please enter right field")
        else:
            #   정상적으로 modify로 이동시켜준다.
            form = TheaterWinBookRecordForm(instance=target_record)  # forms.py의 PostForm 클래스의 인스턴스
            return render(request, 'TheaterWinBook/winbook_modify.html',
                          {'form': form, 'record_pk': record_pk, 'target_record': target_record})

    else:
        #  유저가 확인이 안되면 에러 페이지로 넘김.
        return render(request, 'TheaterWinBook/error_wronguser.html')


@login_required(login_url='/login_view')
def list_usercheck(request):
    print("this is user_check")
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
    if target_record.user_name == login_user:
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
        print("this is post1")
        form = TheaterWinBookRecordForm(request.POST)  # PostForm으로 부터 받은 데이터를 처리하기 위한 인스턴스 생성
        if form.is_valid():  # 폼 검증 메소드
            print("this is post2")
            inputForm = form.save(commit=False)  # 오브젝트를 form으로 부터 가져오지만, 실제로 DB반영은 하지 않는다.
            # 가져 온 후 데이터 처리를 해도 된다.
            inputForm.user_name = request.user
            # inputForm 저장하기
            inputForm.save()
            # 저장한 후에 pk 값 가져오기
            print("this is after saving records pk :", inputForm.pk);
            new_winbook_pk = inputForm.pk
            messages.success(request, 'insert_success', extra_tags=new_winbook_pk)
            # 정보를 성공적으로 입력한 후에는, 메세지에 방금 입력된 pk값을 담아서 보내기
            print("this is post3")
            return redirect('winbook_list')
        else:
            print("this is post4")
            messages.error(request, "please enter right field");

    else:
        form = TheaterWinBookRecordForm()  # forms.py의 PostForm 클래스의 인스턴스
    return render(request, 'TheaterWinBook/winbook_insert.html', {'form': form})  # 템플릿 파일 경로 지정, 데이터 전달


@login_required(login_url='/login_view')
def winbook_statistics(request):
    # 로그인된 user를 확인하고
    login_user_name = request.user
    winbook_user_result = TheaterWinBookRecord.objects.filter(user_name=login_user_name).order_by('buy_date',
                                                                                                  '-pk')
    winbook_user_result_json = serializers.serialize('json', winbook_user_result)

    return render(request, 'TheaterWinBook/winbook_statistics.html',
                  {"winbook_user_result_json": winbook_user_result_json})


# 통계 페이지 기간 설정을 위한 AJAX
@login_required(login_url='/login_view')
def winbook_statistics_ajax(request):
    print("this is winbook_statistics_ajax:")
    datepicker_start = request.GET.get('datepicker_start', None)
    datepicker_end = request.GET.get('datepicker_end', None)
    print("this is datepicker_start:", datepicker_start, "and datepicker_end:", datepicker_end)
    # 기간안의 데이터를 DB에서 검색시작
    # 로그인된 user를 확인하고 해당 user 의 기록을 전부 가지고 오자.
    login_user_name = request.user
    winbook_user_result = TheaterWinBookRecord.objects.filter(user_name=login_user_name,
                                                              buy_date__range=[datepicker_start,
                                                                               datepicker_end]).order_by('buy_date',
                                                                                                         '-pk')
    winbook_user_result_json = serializers.serialize('json', winbook_user_result)
    print("this is json:" + winbook_user_result_json)

    data = {
        'winbook_user_result_json': winbook_user_result_json
    }
    print("this is send:", data)
    return JsonResponse(data)


@login_required(login_url='/login_view')
def winbook_list(request):
    datepicker_start = request.GET.get('datepicker_start', None)
    datepicker_end = request.GET.get('datepicker_end', None)
    pagenum = request.GET.get('pagenum', 1)
    # GET 으로 받은 파라미터는 integer가 아니라, int 처리해줘야 한다....
    pagenum = int(pagenum)

    print("this is datepicker_start:", datepicker_start, "and datepicker_end:", datepicker_end)
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
    if (datepicker_start == None and datepicker_end == None):
        datepicker_start = '2000-01-01'
        datepicker_end = '2100-01-01'
        winbook_user_result = TheaterWinBookRecord.objects.filter(user_name=login_user_name).order_by('-buy_date',
                                                                                                      '-pk')
    else:
        winbook_user_result = TheaterWinBookRecord.objects.filter(user_name=login_user_name,
                                                                  buy_date__range=[datepicker_start,
                                                                                   datepicker_end]).order_by(
            '-buy_date',
            '-pk')

    winbook_user_result_list = list(winbook_user_result)
    total_records_count = len(winbook_user_result_list)
    total_net_profit = 0
    yet_total = 0
    for listobject in winbook_user_result_list:
        win_check = listobject.win_check
        batting_money = listobject.batting_money
        batting_ratio = listobject.batting_ratio
        folder_num = listobject.folder_num
        net_profit = 0
        yet_money = 0
        if win_check == 0:
            net_profit = -(batting_money)
        elif win_check == 1:
            net_profit = ((batting_ratio * batting_money) - (batting_money))
            # 미적중은 total에 카운팅하지 않기로 했다.
        elif win_check == 2:
            yet_money = ((batting_ratio * batting_money) - (batting_money))
        # net_profit = ((batting_ratio * batting_money) - (batting_money))
        total_net_profit += net_profit
        yet_total += yet_money
    total_net_profit = format(int(total_net_profit), ',')
    yet_total = format(int(yet_total), ',')
    # 현재까지 순수익 구하기.

    # 페이지 nator를 사용해서 10개씩 페이지로 만들기.
    paginator = Paginator(winbook_user_result, 10)
    print("this is paginator:", paginator)
    try:
        database_list_result_page = paginator.page(pagenum)
        database_list_result_page.page_range = paginator.page_range
        print("this is database_list_result_page page:", database_list_result_page.page_range)
        total_page_number = paginator.num_pages
        # 페이지에 보이는 페이지 numer의 수
        pagenum_in_per_page = int(10)
        start_page = ((pagenum - 1) // pagenum_in_per_page) * pagenum_in_per_page + 1
        end_page = start_page + pagenum_in_per_page
        if end_page > total_page_number:
            end_page = total_page_number + 1
        print("this is start_page:", start_page)
        database_list_result_page.start_page = int(start_page)
        database_list_result_page.end_page = int(end_page)
        print("this is end_page:", database_list_result_page.end_page)
        database_list_result_page.custom_page_range = range(database_list_result_page.start_page,
                                                            database_list_result_page.end_page)
        database_list_result_page.pagenum = pagenum
        database_list_result_page.total_page_number = total_page_number
    except PageNotAnInteger:
        print("this is not an integer")
        database_list_result_page = paginator.page(1)
    except Exception as e:
        print("this is page exception")
        # 에러가 나면 다시 1페이지로로 돌려주자.
        trace_back = traceback.format_exc()
        message = str(e) + " " + str(trace_back)
        return redirect('winbook_list')

    return render(request, 'TheaterWinBook/winbook_list.html',
                  {"database_list_result_page": database_list_result_page, "new_winbook_pk": new_winbook_pk,
                   'new_winbook_check': new_winbook_check, "total_net_profit": total_net_profit,
                   "yet_total": yet_total, "datepicker_start": datepicker_start, "datepicker_end": datepicker_end,
                   "total_records_count": total_records_count})


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


# 아이디 중복 체크를 위한 AJAX
def kakaoapi_test(request):
    return render(request, 'TheaterWinBook/kakaoapi_test.html')


def question_list(request):
    pagenum = request.GET.get('pagenum', 1)
    # GET 으로 받은 파라미터는 integer가 아니라, int 처리해줘야 한다....
    pagenum = int(pagenum)
    print("this is pagenum", pagenum)
    database_list_result = TheaterWinQuestion.objects.order_by('-question_groupnum', 'question_sequencenum_ingroup')
    # 하나의 페이지당 들어갈 row 개수
    paginator = Paginator(database_list_result, 10)
    print("this is paginator:", paginator)
    try:
        database_list_result_page = paginator.page(pagenum)
        database_list_result_page.page_range = paginator.page_range
        print("this is database_list_result_page page:", database_list_result_page.page_range)
        total_page_number = paginator.num_pages
        # 페이지에 보이는 페이지 numer의 수
        pagenum_in_per_page = int(10)
        start_page = ((pagenum - 1) // pagenum_in_per_page) * pagenum_in_per_page + 1
        end_page = start_page + pagenum_in_per_page
        if end_page > total_page_number:
            end_page = total_page_number + 1
        print("this is start_page:", start_page)
        database_list_result_page.start_page = int(start_page)
        database_list_result_page.end_page = int(end_page)
        print("this is end_page:", database_list_result_page.end_page)
        database_list_result_page.custom_page_range = range(database_list_result_page.start_page,
                                                            database_list_result_page.end_page)
        database_list_result_page.pagenum = pagenum
        database_list_result_page.total_page_number = total_page_number
    except PageNotAnInteger:
        print("this is not an integer")
        database_list_result_page = paginator.page(1)
    except Exception as e:
        print("this is page exception")
        # 에러가 나면 다시 1페이지로로 돌려주자.
        trace_back = traceback.format_exc()
        message = str(e) + " " + str(trace_back)
        return redirect('question_list')
    return render(request, 'TheaterWinBook/question_list.html',
                  {"database_list_result_page": database_list_result_page})


@login_required(login_url='/login_view')
def question_write(request):
    print("this is queistion write")
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = TheaterWinQuestionForm(request.POST)  # PostForm으로 부터 받은 데이터를 처리하기 위한 인스턴스 생성
        is_original = request.POST.get('is_original')
        if is_original == 'question_original':
            # 새로운 글인지 확인)
            # 1. question record에서 가장 높은 pk를 구하고 그것을 +1 해준다.
            # 2-1. groupnm 에 넣어준다 (첫 글 생성일 경우)
            print("this is isoriginal test", is_original)
            if form.is_valid():  # 폼 검증 메소드
                # groupnum 을 pk 로 넣어준다.
                print("this is form is valid:", is_original)
                inputForm = form.save(commit=False)  # 오브젝트를 form으로 부터 가져오지만, 실제로 DB반영은 하지 않는다.
                # 가져 온 후 데이터 처리를 해도 된다.
                inputForm.user_name = request.user
                # inputForm.question_groupnum = 새로 쓴 원본 글이기 때문에 pk 를 groupnum 과 똑같이 해줌.
                inputForm.question_groupnum = int(TheaterWinQuestion.objects.last().pk)
                print("inputForm.pk latest : ", inputForm.question_groupnum)
                # sequence num 을 넣어준다 = 1이다
                inputForm.question_sequencenum_ingroup = 1
                # level 을 넣어준다. 0이다.
                inputForm.question_level_ingroup = 0
                # 데이터베이스에 저장하기
                inputForm.save()
                question_fk = inputForm.pk
                question_record = TheaterWinQuestion.objects.get(pk=question_fk)
                question_info = TheaterWinQuestionInfo(question_fk=question_record)
                question_info.save()
                # question_info 로우를 만들어 준다.
                return redirect('question_list')
            else:
                errors = form.errors.as_data()
                for error in errors:
                    print('There was an error :', error)
                messages.error(request, "please enter right field")
        elif is_original == 'question_reply':
            print("this is question_reply")
            if form.is_valid():  # 폼 검증 메소드
                inputForm = form.save(commit=False)
                parent_question_pk = request.POST.get('question_pk')
                # 부모의 question_pk를 통해서 부모글의 정보를 가져온다.
                parent_question_record = TheaterWinQuestion.objects.get(pk=parent_question_pk)
                parent_question_groupnum = parent_question_record.question_groupnum
                parent_question_sequencenum_ingroup = parent_question_record.question_sequencenum_ingroup
                parent_question_level_ingroup = parent_question_record.question_level_ingorup

                print("this is question_record title:", parent_question_record)
                # groupnum 은 부모 글의 groupnum 과 같다
                # 2-2 해당 글이 댓글잉 경우
                # *공식
                # 1. SELECT NVL(MIN(SORTS),0) FROM BOARD
                #    WHERE  BGROUP = (원글의 BGROUP)
                #    AND SORTS > (원글의 SORTS)
                #    AND DEPTH <= (원글의 DEPTH)
                check = TheaterWinQuestion.objects.filter(question_groupnum=parent_question_groupnum,
                                                          question_sequencenum_ingroup__gt=parent_question_sequencenum_ingroup,
                                                          question_level_ingorup__lte=parent_question_level_ingroup).aggregate(
                    Min('question_sequencenum_ingroup'))["question_sequencenum_ingroup__min"]
                print("this is check:", check);
                # 2-1. 1번이 0 일 경우
                # 3. SELECT NVL(MAX(SORTS),0) + 1 FROM BOARD
                #     WHERE BGROUP = (원글의 BGROUP);
                # 4. INSERT INTO BOARD VALUES
                #    (번호, (원글의 BGROUP), (3번값), (원글의 DEPTH +1) ,' 제목')
                if check is None:
                    check = 0
                if check == 0:
                    new_sequencenum = TheaterWinQuestion.objects.filter(
                        question_groupnum=parent_question_groupnum).aggregate(Max('question_sequencenum_ingroup'))[
                        "question_sequencenum_ingroup__max"]
                    if new_sequencenum is None:
                        new_sequencenum = 0
                    new_sequencenum = new_sequencenum + 1
                    inputForm.question_groupnum = parent_question_groupnum
                    inputForm.question_sequencenum_ingroup = new_sequencenum
                    inputForm.question_level_ingorup = parent_question_level_ingroup + 1
                else:
                    # 2-2. 1번이 0이 아닐 경우
                    #
                    # 3. UPDATE BOARD SET SORTS = SORTS + 1
                    #   WHERE BGROUP =  (원글의 BGROUP)  AND SORTS >= (1번값)
                    TheaterWinQuestion.objects.filter(question_groupnum=parent_question_groupnum,
                                                      question_sequencenum_ingroup__gte=check).update(
                        question_sequencenum_ingroup=F('question_sequencenum_ingroup') + 1)

                    # 4. INSERT INTO BOARD VALUES
                    #    (번호, (원글의 BGROUP), (1번값), (원글의 DEPTH +1) ,' 제목')
                    inputForm.question_groupnum = parent_question_groupnum
                    inputForm.question_sequencenum_ingroup = check
                    inputForm.question_level_ingorup = parent_question_level_ingroup + 1

                # # 데이터베이스에 저장하기
                inputForm.save()
                return redirect('question_list')
            else:
                print("this is question_reply form is not valid")
                messages.error(request, "please enter right field")
    else:
        # 단순히 이동하는 작업이다.
        is_original = request.GET.get('is_original')
        if is_original == 'question_reply':
            # question_pk
            question_pk = request.GET.get('question_pk')
            print("this is question_pk:", question_pk)
            question_record = TheaterWinQuestion.objects.get(pk=question_pk)
            print("this is question_record title:", question_record.question_title)
            question_title = 'RE: ' + question_record.question_title
            form = TheaterWinQuestionForm(initial={'question_title': question_title})  # forms.py의 PostForm 클래스의 인스턴스
        else:
            print("this is is_original is not reply_write")
            form = TheaterWinQuestionForm()  # forms.py의 PostForm 클래스의 인스턴스
    return render(request, 'TheaterWinBook/question_write.html', {'form': form})  # 템플릿 파일 경로 지정, 데이터 전달


@login_required(login_url='/login_view')
def question_detail(request, question_pk):
    is_record_owner = 'not_owner'
    question_pk = question_pk
    # print("this is question_pk" + question_pk)
    target_record = TheaterWinQuestion.objects.get(pk=question_pk)
    # print("this is question_content : " + question_record.question_content)
    form = TheaterWinQuestionForm(instance=target_record)  # forms.py의 PostForm 클래스의 인스턴스
    # 해당 글이 작성자 본인인지 확인 (본인이면 수정,삭제 버튼 누르자)
    login_user = request.user
    if target_record.user_name == login_user:
        is_record_owner = 'owner'
    target_record.question_hit = target_record.question_hit + 1
    target_record.save()

    # 추천과 비추천 숫자를 세자. FOREIGNER 외래키를 찾을 때에는 get이 아니라, filter 를 사용해야 한다.
    thumbup_count = TheaterWinQuestionInfo.objects.filter(question_fk=target_record, question_thumbup=1).count()
    thumbdown_count = TheaterWinQuestionInfo.objects.filter(question_fk=target_record, question_thumbdown=1).count()

    target_replys = TheaterWinQuestionReply.objects.filter(question_fk=target_record)
    return render(request, 'TheaterWinBook/question_detail.html',
                  {'question_record': target_record, 'form': form, 'is_record_owner': is_record_owner,
                   'thumbup_count': thumbup_count, 'thumbdown_count': thumbdown_count, 'target_replys': target_replys,
                   'login_user': login_user})


@login_required(login_url='/login_view')
def winbook_detail(request, record_pk):
    # 1. 해당 리코드의 공개 여부를 확인함.
    winbook_record = TheaterWinBookRecord.objects.get(pk=record_pk)
    winbook_record.hit_count = winbook_record.hit_count + 1
    winbook_record.save()
    share_check = winbook_record.share_check
    form = TheaterWinBookRecordForm(instance=winbook_record)

    # 추천과 비추천 숫자를 세자. FOREIGNER 외래키를 찾을 때에는 get이 아니라, filter 를 사용해야 한다.
    thumbup_count = TheaterWinBookRecordInfo.objects.filter(record_fk=winbook_record, record_thumbup=1).count()
    thumbdown_count = TheaterWinBookRecordInfo.objects.filter(record_fk=winbook_record, record_thumbdown=1).count()
    if share_check == 1:
        #공개로 설정 시에는 전부 공개


        return render(request, 'TheaterWinBook/winbook_detail.html', {'winbook_record': winbook_record, "form": form, "thumbup_count":thumbup_count, "thumbdown_count":thumbdown_count})
    elif share_check ==0:
        login_user_name = request.user
        record_writer = winbook_record.user_name
        if login_user_name == record_writer:
            # 비공개시 그것이 내것이면 접근가능하게 하고
            return render(request, 'TheaterWinBook/winbook_detail.html',
                          {'winbook_record': winbook_record, "form": form,"thumbup_count":thumbdown_count, "thumbdown_count":thumbdown_count})
        else:
            #  유저가 확인이 안되면 에러 페이지로 넘김.
            return render(request, 'TheaterWinBook/error_wronguser.html')


@login_required(login_url='/login_view')
def question_delete(request):
    # request parameter 로 winbook.pk를 받아온다.
    record_pk = request.POST.get("record_pk", "")
    # 받은 pk로 글의 user를 확인한다.
    login_user = request.user
    target_record = TheaterWinQuestion.objects.get(pk=record_pk)
    # 글을 쓴 user와 로그인된 user가 일치하는지 확인
    delete_success = "fail"
    if target_record.user_name == login_user:
        print('this is login user');
        # pk번호를 기준으로 삭제. 삭제는 데이터를 지우는 것이 아니라, title 이랑 content를 수정하는 것으로 하자.
        target_record.question_title = '해당 글은 작성자에 의해 삭제되었습니다.'
        target_record.question_content = '- 해당 글은 작성자에 의해 삭제되었습니다 - '
        target_record.save()
        delete_success = "success";
    else:
        print("this is not equal login user")

    return HttpResponse(json.dumps({'delete_success': delete_success}), content_type="application/json")

    # 일치시에만 삭제 시작하고,

    # else 일치하지 않으면, 잘못된 접근 및 로그아웃 화면으로 넘기자.


@login_required(login_url='/login_view')
def question_modify(request):
    # user를 확인한다
    # 받은 pk로 글의 user를 확인한다.
    record_pk = request.GET.get("record_pk", "")
    login_user = request.user
    target_record = TheaterWinQuestion.objects.get(pk=record_pk)
    print("this is modify1")
    # 글을 쓴 user와 로그인된 user가 일치하는지 확인
    if target_record.user_name == login_user:
        # 수정폼을 제출한 경우.
        print("this is modify2")
        if request.method == "POST":
            print("this is modify3")
            # create a form instance and populate it with data from the request:
            record_pk = request.POST.get("record_pk", "")
            target_modify_record = TheaterWinQuestion.objects.get(pk=record_pk)
            form = TheaterWinQuestionForm(request.POST,
                                          instance=target_modify_record)  # PostForm으로 부터 받은 데이터를 처리하기 위한 인스턴스 생성
            print("this is modify4")
            if form.is_valid():  # 폼 검증 메소드
                print("this is modify5")
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
                return redirect('question_detail', question_pk=modify_winbook_pk)
            else:
                messages.error(request, "please enter right field")
        else:
            #   정상적으로 modify로 이동시켜준다.
            form = TheaterWinQuestionForm(instance=target_record)  # forms.py의 PostForm 클래스의 인스턴스
            return render(request, 'TheaterWinBook/question_modify.html',
                          {'form': form, 'record_pk': record_pk, 'target_record': target_record})
    else:
        #  유저가 확인이 안되면 에러 페이지로 넘김.
        return render(request, 'TheaterWinBook/error_wronguser.html')


@login_required(login_url='/login_view')
def question_usercheck(request):
    print("this is user_check")
    # request parameter 로 winbook.pk를 받아온다.
    record_pk = request.POST.get("record_pk", "")
    # 받은 pk로 글의 user를 확인한다.
    login_user = request.user
    target_record = TheaterWinQuestion.objects.get(pk=record_pk)
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


# CHANNELS 를 이용한 CHATTING 채팅 시작
def full_chatting(request):
    return render(request, 'TheaterWinBook/full_chatting.html')


def chatting_room(request, room_name):
    return render(request, 'TheaterWinBook/chatting_room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


# question 페이지의 thumb up & down 을 위한 AJAX
@login_required(login_url='/login_view')
def question_thumb_ajax(request):
    print("this is question_thumb_ajax:")
    thumb_style = request.POST.get('thumb_style', None)
    target_question_pk = request.POST.get('question_pk', None)
    print("this is target_pk:", target_question_pk)
    login_user_name = request.user
    thumb_result = 'thumb_fail'
    if thumb_style == 'up':
        target_question = TheaterWinQuestion.objects.get(pk=target_question_pk)
        checkobject = TheaterWinQuestionInfo.objects.filter(question_fk__pk=target_question_pk, by_whom=login_user_name,
                                                            question_thumbup=1)
        if not checkobject:
            #     추천한 기록이 없으면
            question_info_record = TheaterWinQuestionInfo(question_fk=target_question, question_thumbup=1,
                                                          by_whom=login_user_name)
            question_info_record.save()
            thumb_result = "up_success"
        else:
            #     만약에 하나라도 있으면, 기존에 있던 추천을 취소하고삭제한다
            checkobject.delete()
            thumb_result = "up_cancel"

    if thumb_style == 'down':
        target_question = TheaterWinQuestion.objects.get(pk=target_question_pk)
        checkobject = TheaterWinQuestionInfo.objects.filter(question_fk__pk=target_question_pk, by_whom=login_user_name,
                                                            question_thumbdown=1)
        if not checkobject:
            #     추천한 기록이 없으면
            question_info_record = TheaterWinQuestionInfo(question_fk=target_question, question_thumbdown=1,
                                                          by_whom=login_user_name)
            question_info_record.save()
            thumb_result = "down_success"
        else:
            #     만약에 하나라도 있으면, 기존에 있던 추천을 취소하고삭제한다
            checkobject.delete()
            thumb_result = "down_cancel"

    data = {
        'thumb_result': thumb_result
    }
    print("this is send:", data)
    return JsonResponse(data)


#  AJAX
@login_required(login_url='/login_view')
def content_reply_ajax(request):
    print("this is content_reply_ajax:")
    question_pk = request.POST.get('question_pk', None)
    print("question_pk", question_pk)
    content_reply = request.POST.get('content_reply', None)
    print("content_reply", content_reply)
    login_user_name = request.user
    question_target = TheaterWinQuestion.objects.get(pk=question_pk)
    content_reply = TheaterWinQuestionReply(question_fk=question_target, question_reply_content=content_reply,
                                            by_whom=login_user_name)
    content_reply.save()
    result = 'success'
    data = {
        'result': result
    }
    print("this is send:", data)
    return JsonResponse(data)


@login_required(login_url='/login_view')
def question_reply_delete(request):
    # request parameter 로 winbook.pk를 받아온다.
    record_pk = request.POST.get("record_pk", "")
    print("this is recordpk," + record_pk)
    # 받은 pk로 글의 user를 확인한다.
    login_user = request.user
    target_record = TheaterWinQuestionReply.objects.get(pk=record_pk)
    # 글을 쓴 user와 로그인된 user가 일치하는지 확인
    delete_success = "fail"
    if target_record.by_whom == login_user:
        print('this is login user');
        # pk번호를 기준으로 삭제. 삭제는 데이터를 지우는 것이 아니라, title 이랑 content를 수정하는 것으로 하자.
        target_record.question_reply_content = '-해당 댓글은 작성자에 의해 삭제되었습니다-'
        target_record.save()
        delete_success = "success";
    else:
        print("this is not equal login user")
    return HttpResponse(json.dumps({'delete_success': delete_success}), content_type="application/json")


@login_required(login_url='/login_view')
def question_reply_modify(request):
    # request parameter 로 winbook.pk를 받아온다.
    record_pk = request.POST.get("record_pk", "")
    print("this is get record_pk", record_pk)
    reply_modify_content = request.POST.get("reply_modify_content")
    print("this is recordpk," + record_pk)
    # 받은 pk로 글의 user를 확인한다.
    login_user = request.user
    target_record = TheaterWinQuestionReply.objects.get(pk=record_pk)
    # 글을 쓴 user와 로그인된 user가 일치하는지 확인
    delete_success = "fail"
    if target_record.by_whom == login_user:
        print('this is login user');
        # pk번호를 기준으로 삭제. 삭제는 데이터를 지우는 것이 아니라, title 이랑 content를 수정하는 것으로 하자.
        target_record.question_reply_content = reply_modify_content
        target_record.save()
        delete_success = "success";
    else:
        print("this is not equal login user")
    return HttpResponse(json.dumps({'delete_success': delete_success}), content_type="application/json")



def share_picks(request):
    pagenum = request.GET.get('pagenum', 1)
    # # GET 으로 받은 파라미터는 integer가 아니라, int 처리해줘야 한다....
    pagenum = int(pagenum)
    winbook_user_result = TheaterWinBookRecord.objects.filter(share_check=1).order_by('-writing_date')
    winbook_user_result_list = list(winbook_user_result)
    total_records_count = len(winbook_user_result_list)
     # 페이지 nator를 사용해서 10개씩 페이지로 만들기.
    paginator = Paginator(winbook_user_result, 10)
    print("this is paginator:", paginator)
    try:
        database_list_result_page = paginator.page(pagenum)
        database_list_result_page.page_range = paginator.page_range
        print("this is database_list_result_page page:", database_list_result_page.page_range)
        total_page_number = paginator.num_pages
        # 페이지에 보이는 페이지 numer의 수
        pagenum_in_per_page = int(10)
        start_page = ((pagenum - 1) // pagenum_in_per_page) * pagenum_in_per_page + 1
        end_page = start_page + pagenum_in_per_page
        if end_page > total_page_number:
            end_page = total_page_number + 1
        print("this is start_page:", start_page)
        database_list_result_page.start_page = int(start_page)
        database_list_result_page.end_page = int(end_page)
        print("this is end_page:", database_list_result_page.end_page)
        database_list_result_page.custom_page_range = range(database_list_result_page.start_page,
                                                            database_list_result_page.end_page)
        database_list_result_page.pagenum = pagenum
        database_list_result_page.total_page_number = total_page_number
    except PageNotAnInteger:
        print("this is not an integer")
        database_list_result_page = paginator.page(1)
    except Exception as e:
        print("this is page exception")
        # 에러가 나면 다시 1페이지로로 돌려주자.
        trace_back = traceback.format_exc()
        message = str(e) + " " + str(trace_back)
        return redirect('winbook_list')

    return render(request, 'TheaterWinBook/share_picks.html',
                  {"database_list_result_page": database_list_result_page, "total_records_count": total_records_count})



@login_required(login_url='/login_view')
def winbook_thumb_ajax(request):
    print("this is winbook_thumb_ajax:")
    thumb_style = request.POST.get('thumb_style', None)
    target_pk = request.POST.get('record_pk', None)
    print("this is target_pk:", target_pk)
    login_user_name = request.user
    thumb_result = 'thumb_fail'
    if thumb_style == 'up':
        target_record = TheaterWinBookRecord.objects.get(pk=target_pk)
        checkobject = TheaterWinBookRecordInfo.objects.filter(record_fk__pk=target_pk, by_whom=login_user_name,
                                                              record_thumbup=1)
        if not checkobject:
            #     추천한 기록이 없으면
            info_record = TheaterWinBookRecordInfo(record_fk=target_record, record_thumbup=1,
                                                          by_whom=login_user_name)
            info_record.save()
            thumb_result = "up_success"
        else:
            #     만약에 하나라도 있으면, 기존에 있던 추천을 취소하고삭제한다
            checkobject.delete()
            thumb_result = "up_cancel"

    if thumb_style == 'down':
        target_record = TheaterWinBookRecord.objects.get(pk=target_pk)
        checkobject = TheaterWinBookRecordInfo.objects.filter(record_fk__pk=target_pk, by_whom=login_user_name,
                                                              record_thumbdown=1)
        if not checkobject:
            #     추천한 기록이 없으면
            info_record = TheaterWinBookRecordInfo(record_fk=target_record, record_thumbdown=1,
                                                          by_whom=login_user_name)
            info_record.save()
            thumb_result = "down_success"
        else:
            #     만약에 하나라도 있으면, 기존에 있던 추천을 취소하고삭제한다
            checkobject.delete()
            thumb_result = "down_cancel"

    data = {
        'thumb_result': thumb_result
    }
    print("this is send:", data)
    return JsonResponse(data)

#  AJAX
@login_required(login_url='/login_view')
def winbook_reply_ajax(request):
    print("this is winbook_reply_ajax:")
    question_pk = request.POST.get('question_pk', None)
    print("question_pk", question_pk)
    content_reply = request.POST.get('content_reply', None)
    print("content_reply", content_reply)
    login_user_name = request.user
    question_target = TheaterWinQuestion.objects.get(pk=question_pk)
    content_reply = TheaterWinQuestionReply(question_fk=question_target, question_reply_content=content_reply,
                                            by_whom=login_user_name)
    content_reply.save()
    result = 'success'
    data = {
        'result': result
    }
    print("this is send:", data)
    return JsonResponse(data)


@login_required(login_url='/login_view')
def winbook_reply_delete(request):
    # request parameter 로 winbook.pk를 받아온다.
    record_pk = request.POST.get("record_pk", "")
    print("this is recordpk," + record_pk)
    # 받은 pk로 글의 user를 확인한다.
    login_user = request.user
    target_record = TheaterWinQuestionReply.objects.get(pk=record_pk)
    # 글을 쓴 user와 로그인된 user가 일치하는지 확인
    delete_success = "fail"
    if target_record.by_whom == login_user:
        print('this is login user');
        # pk번호를 기준으로 삭제. 삭제는 데이터를 지우는 것이 아니라, title 이랑 content를 수정하는 것으로 하자.
        target_record.question_reply_content = '-해당 댓글은 작성자에 의해 삭제되었습니다-'
        target_record.save()
        delete_success = "success";
    else:
        print("this is not equal login user")
    return HttpResponse(json.dumps({'delete_success': delete_success}), content_type="application/json")


@login_required(login_url='/login_view')
def winbook_reply_modify(request):
    # request parameter 로 winbook.pk를 받아온다.
    record_pk = request.POST.get("record_pk", "")
    print("this is get record_pk", record_pk)
    reply_modify_content = request.POST.get("reply_modify_content")
    print("this is recordpk," + record_pk)
    # 받은 pk로 글의 user를 확인한다.
    login_user = request.user
    target_record = TheaterWinQuestionReply.objects.get(pk=record_pk)
    # 글을 쓴 user와 로그인된 user가 일치하는지 확인
    delete_success = "fail"
    if target_record.by_whom == login_user:
        print('this is login user');
        # pk번호를 기준으로 삭제. 삭제는 데이터를 지우는 것이 아니라, title 이랑 content를 수정하는 것으로 하자.
        target_record.question_reply_content = reply_modify_content
        target_record.save()
        delete_success = "success";
    else:
        print("this is not equal login user")
    return HttpResponse(json.dumps({'delete_success': delete_success}), content_type="application/json")
