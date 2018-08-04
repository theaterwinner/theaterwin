from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



class TheaterWinBookRecord(models.Model):
    #토계부 입력에 필요한 데이터들
    buy_date = models.DateField(default=datetime.now, blank=True)
    writing_date = models.DateField(default=datetime.now, blank=False)
    buy_game_title = models.CharField(max_length=200, blank=True)
    batting_ratio = models.FloatField(default=0, blank=True)
    batting_money = models.IntegerField(default=0, blank=True)
    folder_num = models.IntegerField(default=1, blank=True)
    win_check = models.IntegerField(default=1)
    # 장고 모델에서는 null을 허용하지 않고 blank = true로 표시한다.
    etc_memo = models.CharField(blank=True, max_length=200)
    user_name = models.ForeignKey(User,on_delete=models.CASCADE,default=1)


    def __str__(self):
        return self.buy_game_title

