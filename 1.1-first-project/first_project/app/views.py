import datetime
import os
from django.http import HttpResponse
from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'app/home.html'
    pages = {
        'Landing page': reverse('home'),
        'Current time': reverse('time'),
        'Working directory items': reverse('workdir')
    }
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    context = {'local_time': datetime.datetime.now().time()}
    return render(request, 'app/time.html', context)


def workdir_view(request):
    context = {'direct_list': os.listdir()}
    return render(request, 'app/dirlist.html', context)
