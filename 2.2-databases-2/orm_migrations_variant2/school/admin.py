from django.contrib import admin

from .models import Student, Teacher


class StudentTeacherInline(admin.TabularInline):
    model = Student.teachers.through


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']
    list_filter = ['group']
    inlines = [StudentTeacherInline]
    exclude = ['teachers']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'subject']
    list_filter = ['subject']
    inlines = [StudentTeacherInline]
