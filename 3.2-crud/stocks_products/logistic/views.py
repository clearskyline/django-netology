from django.db.models import Q
from django.http import JsonResponse
from rest_framework import pagination
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class CustomPagination(pagination.PageNumberPagination):
    page_size = 2


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # pagination_class = PageNumberPagination  - defined globally
    ordering_fields = ['id', 'title']
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    ordering_fields = ['id', 'address']
    search_fields = ['address']

    def list(self, request, *args, **kwargs):
        prod_id = request.GET.get('products', None)
        if prod_id:
            # получение названия товара - для удобства чтения результата:
            search_product_name = Product.objects.filter(id=prod_id).values('title').get()['title']
            queryset = Stock.objects.filter(products__id=prod_id).values('id', 'address', 'positions__price')
            print(queryset[0]['positions__price'])
            all_stocks = []
            for instance in queryset:
                serializer = StockSerializer(instance)
                req_stock = serializer.data
                all_stocks.append(req_stock)
            return JsonResponse({search_product_name: all_stocks}, json_dumps_params={'ensure_ascii': False})
        search_stock = request.GET.get('search', None)
        if search_stock:
            queryset = Stock.objects.filter(Q(products__title__icontains=search_stock) | Q(products__description__icontains=search_stock)).values('id', 'address')
            required_products = []
            for instance in queryset:
                serializer = StockSerializer(instance)
                req_data = serializer.data
                required_products.append(req_data)
            return JsonResponse({search_stock: required_products}, json_dumps_params={'ensure_ascii': False})
        else:
            queryset = self.filter_queryset(Stock.objects.all())
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            self.pagination_class = CustomPagination
            return self.get_paginated_response(serializer.data)
