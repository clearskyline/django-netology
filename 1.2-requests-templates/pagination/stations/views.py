from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from process_data import data_list


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_num = int(request.GET.get("page", 1))
    paginator = Paginator(data_list, 10)
    bus_st = paginator.get_page(page_num)
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    context = {
        'bus_stations': bus_st,
        # 'page':
    }
    return render(request, 'stations/index.html', context)
