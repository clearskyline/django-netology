from django.contrib.auth.models import User
from rest_framework import serializers
from adv.models import Advertisement, AdvFav
from rest_framework.exceptions import ValidationError


class UserFavsSerializer(serializers.ModelSerializer):
    added_to_favourites = serializers.ReadOnlyField()

    class Meta:
        model = AdvFav
        fields = ['added_to_favourites']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    favourites_by_users = UserFavsSerializer(many=True, required=False)

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'published', 'created_at', 'updated_at', 'favourites_by_users')

    def create(self, validated_data):
        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if (self.context["request"].method == 'POST' and data.get('published') == True and data.get('status') != 'CLOSED') or (self.context["request"].method == 'PATCH' and (data.get('status') == 'OPEN' or data.get('published') == True)):
            open_adv_count = Advertisement.objects.filter(creator=self.context["request"].user, status='OPEN', published=True).count()
            if open_adv_count >= 10:
                raise ValidationError('Too many open ads')
        return data
