# apps/warehouse/elasticsearch/utils.py

from django.conf import settings
from utils.elasticsearch import index_document


# ====================== Warehouse ======================

def create_index_warehouse():
    """
    Create the Elasticsearch index for the Warehouse document.
    """
    index_document(
        index_name='warehouse',
        properties={
            'name': {'type': 'text'},
            'is_active': {'type': 'boolean'},
            'description': {'type': 'text'},
            'is_production_warehouse': {'type': 'boolean'},
        }
    )


def index_warehouse(data: dict):
    """
    Index a Warehouse document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='warehouse',
        id=data['id'],
        document={
            'name': data.get('name', ''),
            'is_active': data.get('is_active', True),
            'description': data.get('description', ''),
            'is_production_warehouse': data.get('is_production_warehouse', True),
        }
    )


def delete_warehouse(document_id: str):
    """
    Delete a Warehouse document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='warehouse', id=document_id):
        es.delete(index='warehouse', id=document_id)


# ====================== Inventory ======================

def create_index_inventory():
    """
    Create the Elasticsearch index for the Inventory document.
    """
    index_document(
        index_name='inventory',
        properties={
            'product': {'type': 'text'},
            'warehouse': {'type': 'text'},
        }
    )


def index_inventory(data: dict):
    """
    Index an Inventory document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='inventory',
        id=data['id'],
        document={
            'product': data.get('product', {}).get('name', 'unknown'),
            'warehouse': data.get('warehouse', {}).get('name', 'unknown'),
        }
    )


def delete_inventory(document_id: str):
    """
    Delete an Inventory document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='inventory', id=document_id):
        es.delete(index='inventory', id=document_id)


# ====================== Transaction ======================

def create_index_transaction():
    """
    Create the Elasticsearch index for the Transaction document.
    """
    index_document(
        index_name='transaction',
        properties={
            'inventory': {'type': 'text'},
            'is_import': {'type': 'boolean'},
            'storage_location': {'type': 'text'},
        }
    )


def index_transaction(data: dict):
    """
    Index a Transaction document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='transaction',
        id=data['id'],
        document={
            'inventory': data.get('inventory', {}).get('id', 'unknown'),
            'is_import': data.get('is_import', True),
            'storage_location': data.get('storage_location', ''),
        }
    )


def delete_transaction(document_id: str):
    """
    Delete a Transaction document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='transaction', id=document_id):
        es.delete(index='transaction', id=document_id)
