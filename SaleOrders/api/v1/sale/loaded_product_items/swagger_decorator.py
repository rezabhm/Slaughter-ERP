from apps.sale.serializer import LoadedProductItemSerializer, LoadedProductItemSerializerPOST
from utils.swagger_utils.custom_swagger_generator import custom_swagger_generator

bulk_post_request_decorator = custom_swagger_generator(serializer_class=LoadedProductItemSerializerPOST, method='bulk_post', many=True)
single_post_request_decorator = custom_swagger_generator(serializer_class=LoadedProductItemSerializerPOST, method='single_post', many=False)
bulk_patch_request_decorator = custom_swagger_generator(serializer_class=LoadedProductItemSerializer, method='bulk_patch', many=True)
single_patch_request_decorator = custom_swagger_generator(serializer_class=LoadedProductItemSerializer, method='single_patch', many=False)
bulk_get_decorator = custom_swagger_generator(serializer_class=LoadedProductItemSerializer, method='bulk_get', many=True)
single_get_decorator = custom_swagger_generator(serializer_class=LoadedProductItemSerializer, method='single_get', many=False)
bulk_delete_request_decorator = custom_swagger_generator(serializer_class=LoadedProductItemSerializer, method='bulk_delete', many=True)
single_delete_request_decorator = custom_swagger_generator(serializer_class=LoadedProductItemSerializer, method='single_delete', many=False)
