from django.db.models import Prefetch
from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


def students_list(request):
    template = 'school/students_list.html'
    all_students = Student.objects.all().order_by('group')
    context = {'object_list': all_students}
    return render(request, template, context)
