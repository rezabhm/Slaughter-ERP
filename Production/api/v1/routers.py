from api.v1.core.views_roles.view import ViewsRolesAPIView
from api.v1.planning.planning_series.view import PlanningSeriesAPIView
from api.v1.planning.planning_series_cell.view import PlanningSeriesCellAPIView
from api.v1.poultry_cutting_production.export_product.view import PoultryCuttingExportProductAPIView
from api.v1.poultry_cutting_production.import_product.view import PoultryCuttingImportProductAPIView
from api.v1.poultry_cutting_production.production_series.view import PoultryCuttingProductionSeriesAPIView
from api.v1.poultry_cutting_production.return_product.view import PoultryCuttingReturnProductAPIView
from api.v1.production.export_product.view import ExportProductAPIView
from api.v1.production.import_product.view import ImportProductByCarAPIView, ImportProductFromWareHouseAPIView
from api.v1.production.production_series.view import ProductionSeriesAPIView
from api.v1.production.return_product.view import ReturnProductAPIView
from utils.CustomRouter.CustomRouter import CustomRouter

default_router = CustomRouter()

default_router.register('core-views-roles', ViewsRolesAPIView)
default_router.register('production/series', ProductionSeriesAPIView)
default_router.register('production/import-product-by-car', ImportProductByCarAPIView)
default_router.register('production/import-product-from-warehouse', ImportProductFromWareHouseAPIView)
default_router.register('production/export-product', ExportProductAPIView)
default_router.register('production/return-product', ReturnProductAPIView)

default_router.register('planning/series', PlanningSeriesAPIView)
default_router.register('planning/cell', PlanningSeriesCellAPIView)

default_router.register('poultry-cutting-production/series', PoultryCuttingProductionSeriesAPIView)
default_router.register('poultry-cutting-production/import-product', PoultryCuttingImportProductAPIView)
default_router.register('poultry-cutting-production/export-product', PoultryCuttingExportProductAPIView)
default_router.register('poultry-cutting-production/return-product', PoultryCuttingReturnProductAPIView)

urlpatterns = default_router.urls

