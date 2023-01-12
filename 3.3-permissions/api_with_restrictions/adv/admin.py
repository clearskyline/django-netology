from adv.models import Advertisement, AdvFav
from django.contrib import admin


class AdvFavInline(admin.TabularInline):
    model = AdvFav
    extra = 1


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'status', 'published', 'creator', 'created_at', 'updated_at']
    inlines = [AdvFavInline, ]


@admin.register(AdvFav)
class AdvFavAdmin(admin.ModelAdmin):
    list_display = ['id', 'users_favorites', 'advert']
