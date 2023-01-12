from adv.views import AdvertisementViewSet
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('advertisements', AdvertisementViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/advertisements/update-fav/<pk>/', AdvertisementViewSet.as_view({"patch": "update_favs"}), name='fav-update-link'),
    path('api/my-favs/', AdvertisementViewSet.as_view({"get": "all_user_favs"}), name='all-user-favourites'),
    path('admin/', admin.site.urls),
]
