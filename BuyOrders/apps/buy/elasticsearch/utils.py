from django.conf import settings

from utils.elasticsearch import index_document


def create_index_production_order_document():
    index_document(
        index_name='production_order',
        properties={

            'car': {'type': 'text'},
            'driver': {'type': 'text'},
            'agriculture': {'type': 'text'},
            'product': {'type': 'text'},
            'product_owner': {'type': 'text'},

        }
    )


def index_product_order(validated_data: dict):
    """
    index data to elasticsearch_api

    Args:
        validated_data: product orders object serializer data
    """
    es = settings.ELASTICSEARCH_CONNECTION

    try:
        car_postfix_number = validated_data['car']['car']['postfix_number']
        car_prefix_number = validated_data['car']['car']['prefix_number']
        car_alphabet = validated_data['car']['car']['alphabet']
        car_city_code = validated_data['car']['car']['city_code']
        car = f'{car_prefix_number}{car_alphabet}{car_postfix_number}-{car_city_code}'

    except Exception:
        car = 'unknown'

    try:
        driver = validated_data['car']['driver']['contact'][0]['name']
    except Exception:
        driver = 'unknown'

    try:
        agriculture = validated_data['order_information']['agriculture']['name']
    except Exception:
        agriculture = 'unknown'

    try:
        product = validated_data['order_information']['product']['name']
    except Exception:
        product = 'unknown'

    try:
        product_owner = validated_data['order_information']['product_owner']['contact']['name']
    except:
        product_owner = 'unknown'

    es.index(

        index='production_order',
        id=str(validated_data['id']),
        document={
            'car': car,
            'driver': driver,
            'agriculture': agriculture,
            'product': product,
            'product_owner': product_owner,
        }

    )


def delete_product_order(document_id: str):
    """
    Delete a document from Elasticsearch index

    Args:
        document_id: ID of document to delete
    """
    es = settings.ELASTICSEARCH_CONNECTION

    if es.exists(index='production_order', id=document_id):
        es.delete(index='production_order', id=document_id)


def search_production_order(keyword: str) -> dict:

    """
    search in production order with keyword

    Args:
        keyword: query params that given from url

    Returns:
        dict: return search results
    """
    es = settings.ELASTICSEARCH_CONNECTION

    return es.search(
        index='production_order',
        query={
            "multi_match": {
                "query": keyword,
                "fields": ["car", "driver", "agriculture", "product", "product_owner"]
            }
        }
    )["hits"]["hits"]
