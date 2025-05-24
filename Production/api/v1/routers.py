from api.v1.production.production_series.production_series_view import ProductionSeriesAPIView
from utils.CustomRouter import CustomRouter

default_router = CustomRouter()

default_router.register('production-series', ProductionSeriesAPIView)

urlpatterns = default_router.urls

