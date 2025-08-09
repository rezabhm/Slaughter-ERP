from api.v1.core.views_roles.view import ViewsRolesAPIView
from api.v1.warehouse.Inventory.view import InventoryAPIView
from api.v1.warehouse.transaction.view import TransactionAPIView
from api.v1.warehouse.warehouse.view import WarehouseAPIView
from rest_framework.routers import DefaultRouter
from utils.CustomRouter.CustomRouter import CustomRouter

router = CustomRouter()

router.register('warehouse', WarehouseAPIView)
router.register('inventory', InventoryAPIView)
router.register('transaction', TransactionAPIView)

drf_router = DefaultRouter()

# drf_router.register('core-views-roles', ViewsRolesAPIView, basename='view-roles')

urlpatterns = router.urls
urlpatterns += drf_router.urls
