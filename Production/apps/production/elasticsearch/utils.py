# apps/production/elasticsearch/utils.py

from django.conf import settings
from utils.elasticsearch import index_document


# ====================== ProductionSeries ======================

def create_index_production_series():
    """
    Create the Elasticsearch index for the ProductionSeries document.
    """
    index_document(
        index_name='production_series',
        properties={
            'product_owner': {'type': 'integer'},
            'status': {'type': 'text'},
        }
    )


def index_production_series(data: dict):
    """
    Index a ProductionSeries document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='production_series',
        id=data['id'],
        document={
            'product_owner': data.get('product_owner', 0),
            'status': data.get('status', 'pending'),
        }
    )


def delete_production_series(document_id: str):
    """
    Delete a ProductionSeries document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='production_series', id=document_id):
        es.delete(index='production_series', id=document_id)


# ====================== ImportProduct ======================

def create_index_import_product():
    """
    Create the Elasticsearch index for the ImportProduct document.
    """
    index_document(
        index_name='import_product',
        properties={
            'agriculture': {'type': 'text'},
            'car': {'type': 'text'},
            'product': {'type': 'text'},
        }
    )


def index_import_product(data: dict):
    """
    Index an ImportProduct document in Elasticsearch.
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
        index='import_product',
        id=data['id'],
        document={
            'agriculture': data.get('agriculture', {}).get('name', 'unknown'),
            'car': car,
            'product': data.get('product', {}).get('name', 'unknown'),
        }
    )


def delete_import_product(document_id: str):
    """
    Delete an ImportProduct document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='import_product', id=document_id):
        es.delete(index='import_product', id=document_id)


# ====================== ImportProductFromWareHouse ======================

def create_index_import_product_from_warehouse():
    """
    Create the Elasticsearch index for the ImportProductFromWareHouse document.
    """
    index_document(
        index_name='import_product_from_warehouse',
        properties={
            'product_description': {'type': 'text'},
        }
    )


def index_import_product_from_warehouse(data: dict):
    """
    Index an ImportProductFromWareHouse document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='import_product_from_warehouse',
        id=data['id'],
        document={
            'product_description': data.get('product_description', {}).get('id', 'unknown'),
        }
    )


def delete_import_product_from_warehouse(document_id: str):
    """
    Delete an ImportProductFromWareHouse document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='import_product_from_warehouse', id=document_id):
        es.delete(index='import_product_from_warehouse', id=document_id)


# ====================== ExportProduct ======================

def create_index_export_product():
    """
    Create the Elasticsearch index for the ExportProduct document.
    """
    index_document(
        index_name='export_product',
        properties={
            'product': {'type': 'text'},
            'receiver_delivery_unit': {'type': 'text'},
        }
    )


def index_export_product(data: dict):
    """
    Index an ExportProduct document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='export_product',
        id=data['id'],
        document={
            'product': data.get('product', 'unknown'),
            'receiver_delivery_unit': data.get('receiver_delivery_unit', ''),
        }
    )


def delete_export_product(document_id: str):
    """
    Delete an ExportProduct document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='export_product', id=document_id):
        es.delete(index='export_product', id=document_id)


# ====================== ReturnProduct ======================

def create_index_return_product():
    """
    Create the Elasticsearch index for the ReturnProduct document.
    """
    index_document(
        index_name='return_product',
        properties={
            'product': {'type': 'text'},
            'return_type': {'type': 'text'},
        }
    )


def index_return_product(data: dict):
    """
    Index a ReturnProduct document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='return_product',
        id=data['id'],
        document={
            'product': data.get('product', {}).get('name', 'unknown'),
            'return_type': data.get('return_type', ''),
        }
    )


def delete_return_product(document_id: str):
    """
    Delete a ReturnProduct document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='return_product', id=document_id):
        es.delete(index='return_product', id=document_id)
