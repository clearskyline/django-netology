from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    all_articles = Article.objects.all().order_by('-published_at')
    context = {'object_list': all_articles}
    return render(request, template, context)
