from api.v1.production.import_product.view import ImportProductByCarAPIView, ImportProductFromWareHouseAPIView
from api.v1.production.production_series.view import ProductionSeriesAPIView
from utils.CustomRouter import CustomRouter

default_router = CustomRouter()

default_router.register('production/series', ProductionSeriesAPIView)
default_router.register('production/import-product-by-car', ImportProductByCarAPIView)
default_router.register('production/import-product-from-warehouse', ImportProductFromWareHouseAPIView)

urlpatterns = default_router.urls

