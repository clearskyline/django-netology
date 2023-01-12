from adv.models import Advertisement, AdvFav
from adv.permissions import IsOwner, IsNotOwner
from adv.serializers import AdvertisementSerializer
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import HttpResponse
from django_filters import DateFromToRangeFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class FilterAds(FilterSet):
    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['created_at']


class AdvertisementViewSet(ModelViewSet):

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    # permission_classes = [IsAuthenticated, IsOwner, IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilterAds

    @staticmethod
    def check_ad_publish_visibility(request):
        if request.user == AnonymousUser():
            visible_queryset = Advertisement.objects.filter(published=True).all()
        else:
            visible_queryset = Advertisement.objects.filter(Q(published=True) | Q(creator_id=request.user)).all()
        return visible_queryset

    def list(self, request, *args, **kwargs):
        visible_queryset = self.check_ad_publish_visibility(request)

        adv_status = request.GET.get('status', None)
        if adv_status:
            queryset = visible_queryset.filter(status__iexact=adv_status)
            serializer = AdvertisementSerializer(queryset, many=True)
            return Response(serializer.data)

        adv_creator = request.GET.get('creator', None)
        if adv_creator:
            queryset = visible_queryset.filter(creator__id=adv_creator)
            serializer = AdvertisementSerializer(queryset, many=True)
            return Response(serializer.data)

        else:
            filter_backends = self.filter_queryset(visible_queryset)
            serializer = AdvertisementSerializer(filter_backends, many=True)
            return Response(serializer.data)

    @action(methods=['PATCH'], detail=True)
    def update_favs(self, request, pk):
        if request.data.get('add to favourites'):
            advert = Advertisement.objects.get(id=pk)
            try:
                AdvFav.objects.get(advert=advert, users_favorites=request.user).delete()
                return HttpResponse(f"Ad was removed from favourites")
            except AdvFav.DoesNotExist:
                AdvFav.objects.create(advert=advert, users_favorites=request.user)
                return HttpResponse(f"Ad was added to favourites")
        return HttpResponse("Command not entered")

    @action(methods=['GET'], detail=True)
    def all_user_favs(self, request):
        visible_queryset = self.check_ad_publish_visibility(request)
        queryset = visible_queryset.filter(favourites=request.user)
        serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data)

    @property
    def permission_classes(self):
        if self.action == "all_user_favs":
            return [IsAuthenticated]
        if self.action == "update_favs":
            return [IsAuthenticated, IsNotOwner]
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated, (IsOwner | IsAdminUser)]
        return []
