# from django.core.exceptions import ObjectDoesNotExist
# from rest_framework import serializers
# 
# from apps.product.models import Unit, ProductCategory, Product
# 
# 
# class UnitSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Unit
#         fields = '__all__'
# 
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
# 
#         try:
#             # ManyToMany relationship: filter products that include this unit
#             products = Product.objects.filter(unit__in=[instance])
#             product_serializer = ProductSerializer(data=products, many=True)
#             product_serializer.is_valid()
#             representation['products'] = product_serializer.data
#         except ObjectDoesNotExist:
#             representation['products'] = []
# 
#         return representation
# 
# 
# class ProductCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductCategory
#         fields = '__all__'
# 
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
# 
#         # Get all products connected to this category
#         try:
#             products = Product.objects.filter(category=instance)
#             product_serializer = ProductSerializer(data=products, many=True)
#             product_serializer.is_valid()
#             representation['products'] = product_serializer.data
#         except ObjectDoesNotExist:
#             representation['products'] = []
# 
#         return representation
# 
# 
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'
# 
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
# 
#         # Handle Product Category (FK)
#         try:
#             category = ProductCategory.objects.get(pk=representation['category'])
#             category_serializer = ProductCategorySerializer(data=[category], many=True)
#             category_serializer.is_valid()
#             representation['category'] = category_serializer.data[0]
#         except ObjectDoesNotExist:
#             representation['category'] = {}
# 
#         # Handle Units (M2M)
#         unit_ids = representation['unit']
#         units = []
#         for unit_id in unit_ids:
#             try:
#                 unit = Unit.objects.get(pk=unit_id)
#                 units.append(unit)
#             except ObjectDoesNotExist:
#                 pass
# 
#         unit_serializer = UnitSerializer(data=units, many=True)
#         unit_serializer.is_valid()
#         representation['unit'] = unit_serializer.data
# 
#         return representation
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from apps.product.models import Unit, ProductCategory, Product


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name', 'slug']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # محصولات را فقط در صورت نیاز و با سریالایزر جداگانه سریال کنید
        return representation


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # محصولات را فقط در صورت نیاز و با سریالایزر جداگانه سریال کنید
        return representation


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    unit = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'code', 'category', 'unit', 'slug']


# سریالایزرهای اضافی برای نمایش محصولات در دسته‌بندی یا واحد
class ProductCategoryWithProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'slug', 'products']

    def get_products(self, obj):
        products = Product.objects.filter(category=obj)[:5]  # محدود کردن تعداد محصولات
        return ProductSerializer(products, many=True, read_only=True).data


class UnitWithProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ['id', 'name', 'slug', 'products']

    def get_products(self, obj):
        products = Product.objects.filter(unit=obj)[:5]  # محدود کردن تعداد محصولات
        return ProductSerializer(products, many=True, read_only=True).data