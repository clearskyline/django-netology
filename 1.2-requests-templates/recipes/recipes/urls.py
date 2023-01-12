
from calculator.views import omelette_view, page_404, landing_page, pasta_view, sandwich_view
from django.urls import path

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('omelette/', omelette_view, name='omelette'),
    path('pasta/', pasta_view, name='pasta'),
    path('sandwich/', sandwich_view, name='sandwich'),
    path('page_404/', page_404, name='page_404')
]

