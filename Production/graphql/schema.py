import graphene

from Production.graphql.export_product_schema import ExportProductQuery
from Production.graphql.import_product_from_warehouse_schema import ImportProductFromWareHouseQuery
from Production.graphql.import_product_schema import ImportProductQuery
from Production.graphql.planning_series_cell_schema import PlanningSeriesCellQuery
from Production.graphql.planning_series_schema import PlanningSeriesQuery
from Production.graphql.poultry_cutting_export_product_schema import PoultryCuttingExportProductQuery
from Production.graphql.poultry_cutting_import_product_schema import PoultryCuttingImportProductQuery
from Production.graphql.poultry_cutting_production_series_schema import PoultryCuttingProductionSeriesQuery
from Production.graphql.poultry_cutting_return_product_schema import PoultryCuttingReturnProductQuery
from Production.graphql.production_series_schema import ProductionSeriesQuery
from Production.graphql.return_product_schema import ReturnProductQuery


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
