from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.accounts.serializers import ContactSerializers
from apps.core.models.ownership import *
from apps.core.models.transportation import Driver, Car
from apps.product.models import ProductCategory
from apps.product.serializers import ProductCategorySerializer


class CitySerializers(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'


class AgricultureSerializers(serializers.ModelSerializer):

    class Meta:
        model = Agriculture
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        try:
            city = City.objects.get(pk=representation['city'])

            city_serializers = CitySerializers(data=[city], many=True)
            city_serializers.is_valid()
            city = city_serializers.data[0]

        except ObjectDoesNotExist:
            city = {}

        representation['city'] = city

        return representation


class ProductOwnerSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProductOwner
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        try:

            contact = Contact.objects.get(pk=representation['contact'])

            contact_serializer = ContactSerializers(data=[contact], many=True)
            contact_serializer.is_valid()
            contact = contact_serializer.data[0]

        except ObjectDoesNotExist:
            contact = {}

        representation['contact'] = contact

        return representation


class DriverSerializers(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        contacts = representation['contact']
        contact_list = []
        for cnt in contacts:

            try:
                contact = Contact.objects.get(pk=cnt)
                contact_list.append(contact)

            except ObjectDoesNotExist:
                pass

        contact_serializers = ContactSerializers(data=contact_list, many=True)
        contact_serializers.is_valid()

        representation['contact'] = contact_serializers.data

        return representation


class CarSerializers(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        try:
            city = City.objects.get(pk=representation['city_code'])

            city_serializers = CitySerializers(data=[city], many=True)
            city_serializers.is_valid()
            city = city_serializers.data[0]

        except ObjectDoesNotExist:
            city = {}

        representation['city'] = city
        representation['city_code'] = city['car_code']

        try:

            product_category = ProductCategory.objects.get(pk=representation['product_category'])
            product_category_serializers = ProductCategorySerializer(data=[product_category], many=True)
            product_category_serializers.is_valid()
            product_category = product_category_serializers.data[0]

        except ObjectDoesNotExist:

            product_category = {}

        representation['product_category'] = product_category

        try:

            driver = Driver.objects.get(pk=representation['driver'])
            driver_serializers = DriverSerializers(data=[driver], many=True)
            driver_serializers.is_valid()
            driver = driver_serializers.data[0]

        except ObjectDoesNotExist:

            driver = {}

        representation['driver'] = driver

        return representation
