# apps/planning/elasticsearch/utils.py

from django.conf import settings
from utils.elasticsearch import index_document


# ====================== PlanningSeries ======================

def create_index_planning_series():
    """
    Create the Elasticsearch index for the PlanningSeries document.
    """
    index_document(
        index_name='planning_series',
        properties={
            'is_finished': {'type': 'boolean'},
        }
    )


def index_planning_series(data: dict):
    """
    Index a PlanningSeries document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='planning_series',
        id=data['id'],
        document={
            'is_finished': data.get('is_finished', False),
        }
    )


def delete_planning_series(document_id: str):
    """
    Delete a PlanningSeries document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='planning_series', id=document_id):
        es.delete(index='planning_series', id=document_id)


# ====================== PlanningSeriesCell ======================

def create_index_planning_series_cell():
    """
    Create the Elasticsearch index for the PlanningSeriesCell document.
    """
    index_document(
        index_name='planning_series_cell',
        properties={
            'import_type': {'type': 'text'},
            'import_id': {'type': 'text'},
        }
    )


def index_planning_series_cell(data: dict):
    """
    Index a PlanningSeriesCell document in Elasticsearch.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='planning_series_cell',
        id=data['id'],
        document={
            'import_type': data.get('import_type', ''),
            'import_id': data.get('import_id', ''),
        }
    )


def delete_planning_series_cell(document_id: str):
    """
    Delete a PlanningSeriesCell document from the Elasticsearch index.
    """
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='planning_series_cell', id=document_id):
        es.delete(index='planning_series_cell', id=document_id)
