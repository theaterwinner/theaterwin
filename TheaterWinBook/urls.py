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

]