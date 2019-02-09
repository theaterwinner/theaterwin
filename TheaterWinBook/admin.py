from django.contrib import admin
from .models import Post,TheaterWinBookRecord,TheaterWinQuestion, TheaterWinQuestionInfo,TheaterWinQuestionReply, Full_Chatting_Message

admin.site.register(Post)
admin.site.register(TheaterWinBookRecord)
admin.site.register(TheaterWinQuestion)
admin.site.register(TheaterWinQuestionInfo)
admin.site.register(TheaterWinQuestionReply)
admin.site.register(Full_Chatting_Message)