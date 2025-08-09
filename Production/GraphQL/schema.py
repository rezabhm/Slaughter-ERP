import graphene

from GraphQL.export_product_schema import ExportProductQuery
from GraphQL.import_product_from_warehouse_schema import ImportProductFromWareHouseQuery
from GraphQL.import_product_schema import ImportProductQuery
from GraphQL.planning_series_cell_schema import PlanningSeriesCellQuery
from GraphQL.planning_series_schema import PlanningSeriesQuery
from GraphQL.poultry_cutting_export_product_schema import PoultryCuttingExportProductQuery
from GraphQL.poultry_cutting_import_product_schema import PoultryCuttingImportProductQuery
from GraphQL.poultry_cutting_production_series_schema import PoultryCuttingProductionSeriesQuery
from GraphQL.poultry_cutting_return_product_schema import PoultryCuttingReturnProductQuery
from GraphQL.production_series_schema import ProductionSeriesQuery
from GraphQL.return_product_schema import ReturnProductQuery


class Query(
    PlanningSeriesQuery,
    PlanningSeriesCellQuery,
    PoultryCuttingProductionSeriesQuery,
    PoultryCuttingImportProductQuery,
    PoultryCuttingExportProductQuery,
    PoultryCuttingReturnProductQuery,
    ProductionSeriesQuery,
    ImportProductQuery,
    ImportProductFromWareHouseQuery,
    ExportProductQuery,
    ReturnProductQuery,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
