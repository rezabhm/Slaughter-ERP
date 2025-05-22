from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

# from api.v1.planning.planning_series_cell_view import PlanningSeriesCellCRUDAPIView
# from api.v1.planning.planning_series_view import PlanningSeriesCRUDAPIView
# from api.v1.poultry_cutting_production.export_product_view import PoultryCuttingExportProductCRUDAPIView
# from api.v1.poultry_cutting_production.import_product_view import PoultryCuttingImportProductCRUDAPIView
# from api.v1.poultry_cutting_production.production_series_view import PoultryCuttingProductionSeriesCRUDAPIView
# from api.v1.poultry_cutting_production.return_product_view import PoultryCuttingReturnProductCRUDAPIView
# from api.v1.production.export_product_view import ExportProductCRUDAPIView
# from api.v1.production.import_product_view import ImportProductCRUDAPIView, ImportProductFromWarHouseCRUDAPIView
from api.v1.production.production_series_view import TestAPIView
from utils.CustomRouter import CustomRouter

# from api.v1.production.return_product_view import ReturnProductCRUDAPIView

router = DefaultRouter()

# # production
# router.register('production/series', ProductionSeriesCRUDAPIView, basename='production-series')
# router.register('production/import-product/car', ImportProductCRUDAPIView, basename='production-import-product-car')
# router.register('production/import-product/warehouse', ImportProductFromWarHouseCRUDAPIView, basename='production-import-product-warehouse')
# router.register('production/export-product', ExportProductCRUDAPIView, basename='production-export-product')
# router.register('production/return-product', ReturnProductCRUDAPIView, basename='production-return-product')
#
# # poultry cutting production
# router.register('poultry-cutting/production-series', PoultryCuttingProductionSeriesCRUDAPIView, basename='poultry-cutting-production-series')
# router.register('poultry-cutting/import-product', PoultryCuttingImportProductCRUDAPIView, basename='poultry-cutting-import-product')
# router.register('poultry-cutting/export-product', PoultryCuttingExportProductCRUDAPIView, basename='poultry-cutting-export-product')
# router.register('poultry-cutting/return-product', PoultryCuttingReturnProductCRUDAPIView, basename='poultry-cutting-return-product')
#
# # planning
# router.register('planning/series', PlanningSeriesCRUDAPIView, basename='planning-series')
# router.register('planning/cell', PlanningSeriesCellCRUDAPIView, basename='planning-cell')
#
# urlpatterns = router.urls


# urlpatterns = [
#
#     path('test/', TestAPIView.as_view({
#
#         'get': 'get_request',
#         'post':'post_request'
#
#     })),                               # list get, single and bulk post create
#     path('test/<slug_field>/', TestAPIView.as_view({
#
#         'get': 'get_request'
#
#     })),                  # get data for slug_field id
#     path('test/p/', TestAPIView.as_view({
#
#         'post': 'action_test'
#     })),                             # bulk perform action with different action type in data
#
#
# ]

default_router = CustomRouter()
default_router.register('test', TestAPIView)
urlpatterns = default_router.urls

