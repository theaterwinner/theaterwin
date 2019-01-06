from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^index_real/$', views.index_real, name='index_real'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^winbook_list/$', views.winbook_list, name='winbook_list'),
    url(r'^winbook_list/(?P<startdate>[\w\-]+)/(?P<enddate>[\w\-]+)/$', views.winbook_list, name='winbook_list'),
    url(r'^winbook_insert/$', views.winbook_insert, name='winbook_insert'),
    url(r'^to_winnerBros/$', views.to_winnerBros, name='to_winnerBros'),
    url(r'^login_view/$', views.login_view, name='login_view'),
    url(r'^logout/$',  auth_views.LogoutView.as_view(), {'next_page': '/'}),  # 로그아웃 후 홈으로 이동
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^winbook_statistics/$', views.winbook_statistics, name='winbook_statistics'),
    url(r'^winbook_calendar/$', views.winbook_calendar, name='winbook_calendar'),
    url(r'^index_video_test/$', views.index_video_test, name='index_video_test'),
    url(r'^list_delete/$', views.list_delete, name='list_delete'),
    url(r'^list_usercheck/$', views.list_usercheck, name='list_usercheck'),
    url(r'^winbook_modify/$', views.winbook_modify, name='winbook_modify'),
    url(r'^error_404/$', views.error_404, name='error_404'),
    url(r'^error_wronguser/$', views.error_wronguser, name='error_wronguser'),
    # url(r'^bower_test/$', views.bower_test, name='bower_test'),
    url(r'^calendar_test/$', views.calendar_test, name='calendar_test'),
    url(r'^winbook_detail/(?P<record_pk>\d+)/$', views.winbook_detail, name='winbook_detail'),
    url(r'^kakaoapi_test/$', views.kakaoapi_test, name='kakaoapi_test'),
    url(r'^ajax/winbook_statistics_ajax/$', views.winbook_statistics_ajax, name='winbook_statistics_ajax'),
    url(r'^question_list/$', views.question_list, name='question_list'),
    url(r'^question_write/$', views.question_write, name='question_write'),
    # 답글을 의미한다.
    url(r'^question_write/(?P<question_pk>\d+)/$', views.question_write, name='question_write'),
    # 파라미터가 있는 url 은 2개가 동시에 필요하다. 기본 url + 파라미터 있는 url
    # url(r'^question_detail/$', views.question_detail, name='question_detail'),
    url(r'^question_detail/(?P<question_pk>\d+)/$', views.question_detail, name='question_detail'),
    url(r'^question_delete/$', views.question_delete, name='question_delete'),
    url(r'^question_modify/$', views.question_modify, name='question_modify'),
    url(r'^question_usercheck/$', views.question_usercheck, name='question_usercheck'),
    # editor wyswig
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^full_chatting/$', views.full_chatting, name='full_chatting'),




]
