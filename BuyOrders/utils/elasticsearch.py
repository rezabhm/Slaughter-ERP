from django.conf import settings


def index_document(index_name: str, properties: dict):
    """
    index document if dose not exist

    Args:
         index_name: document index name in elasticsearch
         properties: documents fields in elasticsearch

    """
    es = settings.ELASTICSEARCH_CONNECTION

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={
            "mappings": {
                "properties": properties
            }
        })
