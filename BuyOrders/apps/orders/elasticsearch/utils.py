from django.conf import settings
from utils.elasticsearch import index_document


# ====================== ProductionOrder ======================

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


def index_production_order(validated_data: dict):
    es = settings.ELASTICSEARCH_CONNECTION

    try:
        car = f"{validated_data['car']['car']['prefix_number']}{validated_data['car']['car']['alphabet']}{validated_data['car']['car']['postfix_number']}-{validated_data['car']['car']['city_code']}"
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


def delete_production_order(document_id: str):
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='production_order', id=document_id):
        es.delete(index='production_order', id=document_id)


def search_production_order(keyword: str) -> dict:
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


# ====================== BankAccount ======================

def create_index_bank_account():
    index_document(
        index_name='bank_account',
        properties={
            'owner_name': {'type': 'text'},
            'account_number': {'type': 'text'},
        }
    )


def index_bank_account(data: dict):
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='bank_account',
        id=data['id'],
        document={
            'owner_name': data.get('owner_name', ''),
            'account_number': data.get('account_number', ''),
        }
    )


def delete_bank_account(document_id: str):
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='bank_account', id=document_id):
        es.delete(index='bank_account', id=document_id)


# ====================== Seller ======================

def create_index_seller():
    index_document(
        index_name='seller',
        properties={
            'name': {'type': 'text'},
            'bank_account': {'type': 'text'},
        }
    )


def index_seller(data: dict):
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='seller',
        id=data['id'],
        document={
            'name': data.get('name', ''),
            'bank_account': data.get('bank_account', ''),
        }
    )


def delete_seller(document_id: str):
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='seller', id=document_id):
        es.delete(index='seller', id=document_id)


# ====================== ProductInformation ======================

def create_index_product_information():
    index_document(
        index_name='product_information',
        properties={
            'product_name': {'type': 'text'},
            'quantity': {'type': 'integer'},
            'unit': {'type': 'text'},
        }
    )


def index_product_information(data: dict):
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='product_information',
        id=data['id'],
        document={
            'product_name': data.get('product_name', ''),
            'quantity': data.get('quantity', 0),
            'unit': data.get('unit', ''),
        }
    )


def delete_product_information(document_id: str):
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='product_information', id=document_id):
        es.delete(index='product_information', id=document_id)


# ====================== PurchaseOrder ======================

def create_index_purchase_order():
    index_document(
        index_name='purchase_order',
        properties={
            'status': {'type': 'text'},
            'product_name': {'type': 'text'},
            'estimated_price': {'type': 'integer'},
            'final_price': {'type': 'integer'},
        }
    )


def index_purchase_order(data: dict):
    es = settings.ELASTICSEARCH_CONNECTION
    product_name = data.get('product', {}).get('product_name', 'unknown')

    es.index(
        index='purchase_order',
        id=data['id'],
        document={
            'status': data.get('status', ''),
            'product_name': product_name,
            'estimated_price': data.get('estimated_price', 0),
            'final_price': data.get('final_price', 0),
        }
    )


def delete_purchase_order(document_id: str):
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='purchase_order', id=document_id):
        es.delete(index='purchase_order', id=document_id)


# ====================== Invoice ======================

def create_index_invoice():
    index_document(
        index_name='invoice',
        properties={
            'invoice_number': {'type': 'text'},
            'title': {'type': 'text'},
            'description': {'type': 'text'},
            'seller': {'type': 'text'},
        }
    )


def index_invoice(data: dict):
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='invoice',
        id=data['id'],
        document={
            'invoice_number': data.get('invoice_number', ''),
            'title': data.get('title', ''),
            'description': data.get('description', ''),
            'seller': data.get('seller', {}).get('name', 'unknown'),
        }
    )


def delete_invoice(document_id: str):
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='invoice', id=document_id):
        es.delete(index='invoice', id=document_id)


# ====================== Payment ======================

def create_index_payment():
    index_document(
        index_name='payment',
        properties={
            'amount': {'type': 'integer'},
            'payment_type': {'type': 'text'},
            'from_account': {'type': 'text'},
            'to_account': {'type': 'text'},
        }
    )


def index_payment(data: dict):
    es = settings.ELASTICSEARCH_CONNECTION
    es.index(
        index='payment',
        id=data['id'],
        document={
            'amount': data.get('amount', 0),
            'payment_type': data.get('payment_type', ''),
            'from_account': data.get('from_account', {}).get('account_number', 'unknown'),
            'to_account': data.get('to_account', {}).get('account_number', 'unknown'),
        }
    )


def delete_payment(document_id: str):
    es = settings.ELASTICSEARCH_CONNECTION
    if es.exists(index='payment', id=document_id):
        es.delete(index='payment', id=document_id)
