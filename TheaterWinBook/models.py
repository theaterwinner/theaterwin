from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime
from tinymce import HTMLField


class TheaterWinQuestion(models.Model):
    # 토계부 질문게시판용 필드 모델
    writing_date = models.DateField(default=datetime.now, blank=False)
    question_title = models.CharField(max_length=200, blank=False)
    question_content = HTMLField('Content')
    # isanswer 은 답변이 달렸는지에 대한 필드, 0이면 안 달리고 1이면 달린것이다.
    question_isanswer = models.IntegerField(default=0, blank=False)
    question_thumbup = models.IntegerField(default=0, blank=False)
    question_hit = models.IntegerField(default=0, blank=False)
    # 계층형 답변 게시물을 위한 필드
    question_groupnum =  models.IntegerField(default=0, blank=False)
    question_sequencenum_ingroup =  models.IntegerField(default=0, blank=False)
    question_level_ingorup = models.IntegerField(default=0, blank=False)
    # 기타 메모 및 유저 네임 필드
    etc_memo = models.CharField(blank=True, max_length=200)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def publish(self):
        self.writing_date = timezone.now()
        self.save()

    def __str__(self):
        return self.question_title


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    created_date2 = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class TheaterWinBookRecord(models.Model):
    # 토계부 입력에 필요한 데이터들
    buy_date = models.DateField(default=datetime.now, blank=True)
    writing_date = models.DateField(default=datetime.now, blank=False)
    buy_game_title = models.CharField(max_length=200, blank=True)
    batting_ratio = models.FloatField(default=0, blank=True)
    batting_money = models.IntegerField(default=0, blank=True)
    folder_num = models.IntegerField(default=1, blank=True)
    win_check = models.IntegerField(default=1)
    # 장고 모델에서는 null을 허용하지 않고 blank = true로 표시한다.
    etc_memo = models.CharField(blank=True, max_length=200)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.buy_game_title


