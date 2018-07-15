from django.shortcuts import render

# Create your views here.
def post_list(request):
    return render(request, 'TheaterWinBook/post_list.html', {})