from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_entry = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                main_entry += 1
        if main_entry != 1:
            raise ValidationError('Укажите один основной раздел')
        return super().clean()


class ArticleScopeInline(admin.TabularInline):
    model = Scope
    extra = 0
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'published_at', 'image']
    list_filter = ['published_at']
    inlines = [ArticleScopeInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

