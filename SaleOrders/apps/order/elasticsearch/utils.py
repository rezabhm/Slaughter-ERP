# apps/order/elasticsearch/utils.py

from django.conf import settings
from utils.elasticsearch import index_document


# ====================== Order ======================

def create_index_order():
    """
    Create the Elasticsearch index for the Order document.
    """
    index_document(
        index_name='order',
        properties={
            'customer': {'type': 'text'},
            'car': {'type': 'text'},
        }
    )


def index_order(data: dict):
    """
    Index an Order document in Elasticsearch.
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
        index='order',
        id=data['id'],
        document={
            'customer': data.get('customer', ''),
            'car': car,
        }
    )


def delete_order(document_id: str):
    """
    Delete an Order document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='order', id=document_id):
        es.delete(index='order', id=document_id)


# ====================== OrderItem ======================

def create_index_order_item():
    """
    Create the Elasticsearch index for the OrderItem document.
    """
    index_document(
        index_name='order_item',
        properties={
            'product': {'type': 'text'},
            'order': {'type': 'text'},
        }
    )


def index_order_item(data: dict):
    """
    Index an OrderItem document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='order_item',
        id=data['id'],
        document={
            'product': data.get('product', 'unknown'),
            'order': data.get('order', {}).get('id', 'unknown'),
        }
    )


def delete_order_item(document_id: str):
    """
    Delete an OrderItem document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='order_item', id=document_id):
        es.delete(index='order_item', id=document_id)
