from api.v1.core.views_roles.view import ViewsRolesAPIView
from api.v1.order.order.view import OrderAPIView
from api.v1.order.order_item.view import OrderItemAPIView
from api.v1.sale.loaded_product.view import LoadedProductAPIView
from api.v1.sale.loaded_product_items.view import LoadedProductItemAPIView
from api.v1.sale.truck_loading.view import TruckLoadingAPIView
from rest_framework.routers import DefaultRouter
from utils.CustomRouter.CustomRouter import CustomRouter

router = CustomRouter()

router.register('sale/truck-loading', TruckLoadingAPIView)
router.register('sale/loaded-product', LoadedProductAPIView)
router.register('sale/loaded-product-items', LoadedProductItemAPIView)

router.register('order/order', OrderAPIView)
router.register('order/order-items', OrderItemAPIView)

drf_router = DefaultRouter()

# drf_router.register('core-views-roles', ViewsRolesAPIView, basename='view-roles')

urlpatterns = router.urls
urlpatterns += drf_router.urls
