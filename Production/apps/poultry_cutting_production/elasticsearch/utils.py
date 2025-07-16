# apps/poultry_cutting_production/elasticsearch/utils.py

from django.conf import settings
from utils.elasticsearch import index_document


# ====================== PoultryCuttingProductionSeries ======================

def create_index_poultry_cutting_production_series():
    """
    Create the Elasticsearch index for the PoultryCuttingProductionSeries document.
    """
    index_document(
        index_name='poultry_cutting_production_series',
        properties={
            'product_owner': {'type': 'text'},
            'status': {'type': 'text'},
        }
    )


def index_poultry_cutting_production_series(data: dict):
    """
    Index a PoultryCuttingProductionSeries document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='poultry_cutting_production_series',
        id=data['id'],
        document={
            'product_owner': data.get('product_owner', ''),
            'status': data.get('status', 'pending'),
        }
    )


def delete_poultry_cutting_production_series(document_id: str):
    """
    Delete a PoultryCuttingProductionSeries document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='poultry_cutting_production_series', id=document_id):
        es.delete(index='poultry_cutting_production_series', id=document_id)


# ====================== PoultryCuttingImportProduct ======================

def create_index_poultry_cutting_import_product():
    """
    Create the Elasticsearch index for the PoultryCuttingImportProduct document.
    """
    index_document(
        index_name='poultry_cutting_import_product',
        properties={
            'product': {'type': 'text'},
            'dispatch_unit': {'type': 'text'},
        }
    )


def index_poultry_cutting_import_product(data: dict):
    """
    Index a PoultryCuttingImportProduct document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='poultry_cutting_import_product',
        id=data['id'],
        document={
            'product': data.get('product', {}).get('name', 'unknown'),
            'dispatch_unit': data.get('dispatch_unit', ''),
        }
    )


def delete_poultry_cutting_import_product(document_id: str):
    """
    Delete a PoultryCuttingImportProduct document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='poultry_cutting_import_product', id=document_id):
        es.delete(index='poultry_cutting_import_product', id=document_id)


# ====================== PoultryCuttingExportProduct ======================

def create_index_poultry_cutting_export_product():
    """
    Create the Elasticsearch index for the PoultryCuttingExportProduct document.
    """
    index_document(
        index_name='poultry_cutting_export_product',
        properties={
            'product': {'type': 'text'},
            'receiver_delivery_unit': {'type': 'text'},
        }
    )


def index_poultry_cutting_export_product(data: dict):
    """
    Index a PoultryCuttingExportProduct document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='poultry_cutting_export_product',
        id=data['id'],
        document={
            'product': data.get('product', {}).get('name', 'unknown'),
            'receiver_delivery_unit': data.get('receiver_delivery_unit', ''),
        }
    )


def delete_poultry_cutting_export_product(document_id: str):
    """
    Delete a PoultryCuttingExportProduct document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='poultry_cutting_export_product', id=document_id):
        es.delete(index='poultry_cutting_export_product', id=document_id)


# ====================== PoultryCuttingReturnProduct ======================

def create_index_poultry_cutting_return_product():
    """
    Create the Elasticsearch index for the PoultryCuttingReturnProduct document.
    """
    index_document(
        index_name='poultry_cutting_return_product',
        properties={
            'product': {'type': 'text'},
            'return_type': {'type': 'text'},
        }
    )


def index_poultry_cutting_return_product(data: dict):
    """
    Index a PoultryCuttingReturnProduct document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='poultry_cutting_return_product',
        id=data['id'],
        document={
            'product': data.get('product', {}).get('name', 'unknown'),
            'return_type': data.get('return_type', ''),
        }
    )


def delete_poultry_cutting_return_product(document_id: str):
    """
    Delete a PoultryCuttingReturnProduct document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='poultry_cutting_return_product', id=document_id):
        es.delete(index='poultry_cutting_return_product', id=document_id)
