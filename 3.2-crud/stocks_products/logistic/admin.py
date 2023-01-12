from django.contrib import admin
from logistic.models import Product, Stock, StockProduct


class StockProductInline(admin.TabularInline):
    model = StockProduct
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    inlines = [StockProductInline, ]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'address']
    inlines = [StockProductInline, ]


@admin.register(StockProduct)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'stock', 'product', 'quantity', 'price']


