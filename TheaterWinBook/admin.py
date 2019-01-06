from django.contrib import admin
from .models import Post,TheaterWinBookRecord,TheaterWinQuestion

admin.site.register(Post)
admin.site.register(TheaterWinBookRecord)
admin.site.register(TheaterWinQuestion)
