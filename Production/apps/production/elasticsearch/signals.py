# apps/production/elasticsearch/signals.py

from mongoengine import signals
from apps.production.documents import (
    ProductionSeries,
    ImportProduct,
    ImportProductFromWareHouse,
    ExportProduct,
    ReturnProduct,
)
from apps.production.elasticsearch.utils import (
    index_production_series,
    delete_production_series,
    index_import_product,
    delete_import_product,
    index_import_product_from_warehouse,
    delete_import_product_from_warehouse,
    index_export_product,
    delete_export_product,
    index_return_product,
    delete_return_product,
)
from apps.production.serializers.series_serializer import (
    ProductionSeriesSerializer,
)
from apps.production.serializers.import_serializer import (
    ImportProductSerializer,
    ImportProductFromWareHouseSerializer,
)
from apps.production.serializers.export_serializer import (
    ExportProductSerializer,
)
from apps.production.serializers.return_serializer import (
    ReturnProductSerializer,
)


@signals.post_save.connect
def index_production_series_on_save(sender, document, **kwargs):
    """
    Signal to index a ProductionSeries document when it's saved.
    """
    if isinstance(document, ProductionSeries):
        data = ProductionSeriesSerializer(document).data
        index_production_series(data)


@signals.post_delete.connect
def delete_production_series_on_delete(sender, document, **kwargs):
    """
    Signal to delete a ProductionSeries document from the index when it's deleted.
    """
    if isinstance(document, ProductionSeries):
        delete_production_series(str(document.id))


@signals.post_save.connect
def index_import_product_on_save(sender, document, **kwargs):
    """
    Signal to index an ImportProduct document when it's saved.
    """
    if isinstance(document, ImportProduct):
        data = ImportProductSerializer(document).data
        index_import_product(data)


@signals.post_delete.connect
def delete_import_product_on_delete(sender, document, **kwargs):
    """
    Signal to delete an ImportProduct document from the index when it's deleted.
    """
    if isinstance(document, ImportProduct):
        delete_import_product(str(document.id))


@signals.post_save.connect
def index_import_product_from_warehouse_on_save(sender, document, **kwargs):
    """
    Signal to index an ImportProductFromWareHouse document when it's saved.
    """
    if isinstance(document, ImportProductFromWareHouse):
        data = ImportProductFromWareHouseSerializer(document).data
        index_import_product_from_warehouse(data)


@signals.post_delete.connect
def delete_import_product_from_warehouse_on_delete(sender, document, **kwargs):
    """
    Signal to delete an ImportProductFromWareHouse document from the index when it's deleted.
    """
    if isinstance(document, ImportProductFromWareHouse):
        delete_import_product_from_warehouse(str(document.id))


@signals.post_save.connect
def index_export_product_on_save(sender, document, **kwargs):
    """
    Signal to index an ExportProduct document when it's saved.
    """
    if isinstance(document, ExportProduct):
        data = ExportProductSerializer(document).data
        index_export_product(data)


@signals.post_delete.connect
def delete_export_product_on_delete(sender, document, **kwargs):
    """
    Signal to delete an ExportProduct document from the index when it's deleted.
    """
    if isinstance(document, ExportProduct):
        delete_export_product(str(document.id))


@signals.post_save.connect
def index_return_product_on_save(sender, document, **kwargs):
    """
    Signal to index a ReturnProduct document when it's saved.
    """
    if isinstance(document, ReturnProduct):
        data = ReturnProductSerializer(document).data
        index_return_product(data)


@signals.post_delete.connect
def delete_return_product_on_delete(sender, document, **kwargs):
    """
    Signal to delete a ReturnProduct document from the index when it's deleted.
    """
    if isinstance(document, ReturnProduct):
        delete_return_product(str(document.id))
