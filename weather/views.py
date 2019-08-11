from django.shortcuts import render


def home(request):
    return render(request, 'weather/home.html')


def detail(request):
    return render(request, 'weather/detail.html')
