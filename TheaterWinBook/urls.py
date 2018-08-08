from django.conf.urls import url
from django.conf.urls import include, url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^winbook_list/$', views.winbook_list, name='winbook_list'),
    url(r'^winbook_insert/$', views.winbook_insert, name='winbook_insert'),
    url(r'^to_winnerBros/$', views.to_winnerBros, name='to_winnerBros'),
    url(r'^login_view/$', views.login_view, name='login_view'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),  # 로그아웃 후 홈으로 이동
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^winbook_statistics/$', views.winbook_statistics, name='winbook_statistics'),
    url(r'^winbook_calendar/$', views.winbook_calendar, name='winbook_calendar'),
    url(r'^index_video_test/$', views.index_video_test, name='index_video_test'),
    url(r'^list_delete/$', views.list_delete, name='list_delete'),
    url(r'^list_usercheck/$', views.list_usercheck, name='list_usercheck'),
    url(r'^winbook_modify/$', views.winbook_modify, name='winbook_modify'),
    url(r'^error_404/$', views.error_404, name='error_404'),
    url(r'^error_wronguser/$', views.error_wronguser, name='error_wronguser'),
]
