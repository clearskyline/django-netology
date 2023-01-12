from django.contrib import admin

from .models import Student, Teacher, StudentTeacher


class StudentTeacherInline(admin.TabularInline):
    model = StudentTeacher
    extra = 0


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']
    inlines = [StudentTeacherInline, ]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject']

