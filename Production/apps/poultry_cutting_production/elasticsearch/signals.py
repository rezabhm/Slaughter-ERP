# apps/poultry_cutting_production/elasticsearch/signals.py

from mongoengine import signals
from apps.poultry_cutting_production.documents import (
    PoultryCuttingProductionSeries,
    PoultryCuttingImportProduct,
    PoultryCuttingExportProduct,
    PoultryCuttingReturnProduct,
)
from apps.poultry_cutting_production.elasticsearch.utils import (
    index_poultry_cutting_production_series,
    delete_poultry_cutting_production_series,
    index_poultry_cutting_import_product,
    delete_poultry_cutting_import_product,
    index_poultry_cutting_export_product,
    delete_poultry_cutting_export_product,
    index_poultry_cutting_return_product,
    delete_poultry_cutting_return_product,
)
from apps.poultry_cutting_production.serializers.series_serializer import (
    PoultryCuttingProductionSeriesSerializer,
)
from apps.poultry_cutting_production.serializers.import_serializer import (
    PoultryCuttingImportProductSerializer,
)
from apps.poultry_cutting_production.serializers.export_serializer import (
    PoultryCuttingExportProductSerializer,
)
from apps.poultry_cutting_production.serializers.return_serializer import (
    PoultryCuttingReturnProductSerializer,
)


@signals.post_save.connect
def index_poultry_cutting_production_series_on_save(sender, document, **kwargs):
    """
    Signal to index a PoultryCuttingProductionSeries document when it's saved.
    """
    if isinstance(document, PoultryCuttingProductionSeries):
        data = PoultryCuttingProductionSeriesSerializer(document).data
        index_poultry_cutting_production_series(data)


@signals.post_delete.connect
def delete_poultry_cutting_production_series_on_delete(sender, document, **kwargs):
    """
    Signal to delete a PoultryCuttingProductionSeries document from the index when it's deleted.
    """
    if isinstance(document, PoultryCuttingProductionSeries):
        delete_poultry_cutting_production_series(str(document.id))


@signals.post_save.connect
def index_poultry_cutting_import_product_on_save(sender, document, **kwargs):
    """
    Signal to index a PoultryCuttingImportProduct document when it's saved.
    """
    if isinstance(document, PoultryCuttingImportProduct):
        data = PoultryCuttingImportProductSerializer(document).data
        index_poultry_cutting_import_product(data)


@signals.post_delete.connect
def delete_poultry_cutting_import_product_on_delete(sender, document, **kwargs):
    """
    Signal to delete a PoultryCuttingImportProduct document from the index when it's deleted.
    """
    if isinstance(document, PoultryCuttingImportProduct):
        delete_poultry_cutting_import_product(str(document.id))


@signals.post_save.connect
def index_poultry_cutting_export_product_on_save(sender, document, **kwargs):
    """
    Signal to index a PoultryCuttingExportProduct document when it's saved.
    """
    if isinstance(document, PoultryCuttingExportProduct):
        data = PoultryCuttingExportProductSerializer(document).data
        index_poultry_cutting_export_product(data)


@signals.post_delete.connect
def delete_poultry_cutting_export_product_on_delete(sender, document, **kwargs):
    """
    Signal to delete a PoultryCuttingExportProduct document from the index when it's deleted.
    """
    if isinstance(document, PoultryCuttingExportProduct):
        delete_poultry_cutting_export_product(str(document.id))


@signals.post_save.connect
def index_poultry_cutting_return_product_on_save(sender, document, **kwargs):
    """
    Signal to index a PoultryCuttingReturnProduct document when it's saved.
    """
    if isinstance(document, PoultryCuttingReturnProduct):
        data = PoultryCuttingReturnProductSerializer(document).data
        index_poultry_cutting_return_product(data)


@signals.post_delete.connect
def delete_poultry_cutting_return_product_on_delete(sender, document, **kwargs):
    """
    Signal to delete a PoultryCuttingReturnProduct document from the index when it's deleted.
    """
    if isinstance(document, PoultryCuttingReturnProduct):
        delete_poultry_cutting_return_product(str(document.id))
