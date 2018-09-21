import datetime

from django import forms
from django.contrib.auth.models import User
from django.forms.utils import ErrorList

from TheaterWinBook.models import TheaterWinBookRecord, Post


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password','email','first_name']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password'] # 로그인 시에는 유저이름과 비밀번호만 입력 받는다.



class TheaterWinBookRecordForm(forms.ModelForm):
    # record_id
    # 개인적으로 input type의 위젯이 필요하면, 이렇게 바꾼다
    buy_date = forms.DateField(widget=forms.DateInput(attrs={'type':'text','id':'buy_date'}),initial=datetime.date.today)
    writing_date = forms.DateField(widget=forms.DateInput(attrs={'type':'text','id':'writing_date'}),initial=datetime.date.today)
    batting_ratio = forms.FloatField(required=True, max_value=100, min_value=0, widget=forms.NumberInput(attrs={'step': "0.01"}),initial=1)
    batting_money = forms.CharField(required=True, widget=forms.TextInput(attrs={'type':'text'}))
    folder_num = forms.IntegerField(required=True, max_value=1000000, min_value=1, widget=forms.NumberInput(attrs={'step': "1"}), initial=1)
    # choice의 선택지이다. value가 첫 번째이고, 두 번째는 화면에 나타나는 부분.
    win_check_choice = [(0, '적중실패'), (1, '적중성공'), (2, '경기전')]
    win_check = forms.ChoiceField(choices=win_check_choice,initial=1, widget=forms.Select(attrs={'style':'padding:5px 5px; text-align-last:center'}))

    class Meta:
        model = TheaterWinBookRecord
        exclude = ('user_name',)
    # 부트 스트랩을 위한 form class 추가. 모든 필드 widget 특성에 form-control추가.

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control input-lg'
            })



