from logistic.models import Product, StockProduct, Stock
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ProductPositionSerializer(serializers.ModelSerializer):
    stock_name = serializers.ReadOnlyField(source='stock.address')
    product_name = serializers.ReadOnlyField(source='product.title')
    product_description = serializers.ReadOnlyField(source='product.description')

    class Meta:
        model = StockProduct
        fields = ['id', 'stock_name', 'product', 'product_name', 'product_description', 'quantity', 'price']

    def validate(self, attrs):
        # доп. проверка: PositiveIntegerField в модели может принимать значение "0"
        if attrs.get('quantity') <= 0 or attrs.get('price') <= 0:
            raise ValidationError('Invalid quantity or price')
        return attrs


class ProductSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'positions']

    def validate(self, attrs):
        try:
            title_length_check = attrs['title']
            if len(title_length_check) < 3:
                raise ValidationError('Invalid product name')
        except KeyError:
            return attrs
        return attrs


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True, required=False)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def validate(self, attrs):
        try:
            address_length_check = attrs['address']
            if len(address_length_check) < 3:
                raise ValidationError('Invalid stock address')
        except KeyError:
            return attrs
        return attrs

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position_entry in positions:
            StockProduct.objects.create(**position_entry, stock=stock)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)
        for position_entry in positions:
            StockProduct.objects.update_or_create(stock=stock, product=position_entry['product'], defaults={'quantity': position_entry.get('quantity'), 'price': position_entry.get('price')})
        return stock
