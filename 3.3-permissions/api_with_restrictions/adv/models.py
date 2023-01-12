from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"


class Advertisement(models.Model):

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    published = models.BooleanField(blank=True, null=True, default=False)
    favourites = models.ManyToManyField(User, related_name='fav_ads', through='AdvFav')

    def __str__(self):
        return self.title


class AdvFav(models.Model):
    users_favorites = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites_by_users', verbose_name='Users_added_to_favorites', null=True)
    advert = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='favourites_by_users')

    @property
    def added_to_favourites(self):
        return self.users_favorites.username


'''
for future reference:

    @cached_property
    def ad_was_published(self):
        return self.is_published <= timezone.now()

    def publish_ad(self):
        self.is_published = timezone.now()
'''