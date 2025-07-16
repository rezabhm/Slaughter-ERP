from api.v1.order.order.view import OrderAPIView
from api.v1.order.order_item.view import OrderItemAPIView
from api.v1.sale.loaded_product.view import LoadedProductAPIView
from api.v1.sale.loaded_product_items.view import LoadedProductItemAPIView
from api.v1.sale.truck_loading.view import TruckLoadingAPIView
from utils.CustomRouter.CustomRouter import CustomRouter

router = CustomRouter()

router.register('sale/truck-loading', TruckLoadingAPIView)
router.register('sale/loaded-product', LoadedProductAPIView)
router.register('sale/loaded-product-items', LoadedProductItemAPIView)

router.register('order/order', OrderAPIView)
router.register('order/order-items', OrderItemAPIView)

urlpatterns = router.urls
