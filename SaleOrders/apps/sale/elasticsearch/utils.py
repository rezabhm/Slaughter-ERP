# apps/sale/elasticsearch/utils.py

from django.conf import settings
from utils.elasticsearch import index_document


# ====================== TruckLoading ======================

def create_index_truck_loading():
    """
    Create the Elasticsearch index for the TruckLoading document.
    """
    index_document(
        index_name='truck_loading',
        properties={
            'car': {'type': 'text'},
            'buyer': {'type': 'text'},
        }
    )


def index_truck_loading(data: dict):
    """
    Index a TruckLoading document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    try:
        car_postfix_number = data['car']['car']['postfix_number']
        car_prefix_number = data['car']['car']['prefix_number']
        car_alphabet = data['car']['car']['alphabet']
        car_city_code = data['car']['car']['city_code']
        car = f'{car_prefix_number}{car_alphabet}{car_postfix_number}-{car_city_code}'

    except Exception:
        car = 'unknown'
    es.index(
        index='truck_loading',
        id=data['id'],
        document={
            'car': car,
            'buyer': data.get('buyer', ''),
        }
    )


def delete_truck_loading(document_id: str):
    """
    Delete a TruckLoading document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='truck_loading', id=document_id):
        es.delete(index='truck_loading', id=document_id)


# ====================== LoadedProduct ======================

def create_index_loaded_product():
    """
    Create the Elasticsearch index for the LoadedProduct document.
    """
    index_document(
        index_name='loaded_product',
        properties={
            'product': {'type': 'text'},
            'car': {'type': 'text'},
        }
    )


def index_loaded_product(data: dict):
    """
    Index a LoadedProduct document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    try:
        car_postfix_number = data['car']['car']['postfix_number']
        car_prefix_number = data['car']['car']['prefix_number']
        car_alphabet = data['car']['car']['alphabet']
        car_city_code = data['car']['car']['city_code']
        car = f'{car_prefix_number}{car_alphabet}{car_postfix_number}-{car_city_code}'

    except Exception:
        car = 'unknown'
    es.index(
        index='loaded_product',
        id=data['id'],
        document={
            'product': data.get('product', {}).get('name', 'unknown'),
            'car': car,
        }
    )


def delete_loaded_product(document_id: str):
    """
    Delete a LoadedProduct document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='loaded_product', id=document_id):
        es.delete(index='loaded_product', id=document_id)


# ====================== LoadedProductItem ======================

def create_index_loaded_product_item():
    """
    Create the Elasticsearch index for the LoadedProductItem document.
    """
    index_document(
        index_name='loaded_product_item',
        properties={
            'loaded_product': {'type': 'text'},
        }
    )


def index_loaded_product_item(data: dict):
    """
    Index a LoadedProductItem document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='loaded_product_item',
        id=data['id'],
        document={
            'loaded_product': data.get('loaded_product', {}).get('id', 'unknown'),
        }
    )


def delete_loaded_product_item(document_id: str):
    """
    Delete a LoadedProductItem document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='loaded_product_item', id=document_id):
        es.delete(index='loaded_product_item', id=document_id)
