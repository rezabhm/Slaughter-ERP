from api.v1.core.views_roles.view import ViewsRolesAPIView
from api.v1.warehouse.Inventory.view import InventoryAPIView
from api.v1.warehouse.transaction.view import TransactionAPIView
from api.v1.warehouse.warehouse.view import WarehouseAPIView
from utils.CustomRouter.CustomRouter import CustomRouter

router = CustomRouter()

router.register('core-views-roles', ViewsRolesAPIView)
router.register('warehouse', WarehouseAPIView)
router.register('inventory', InventoryAPIView)
router.register('transaction', TransactionAPIView)

urlpatterns = router.urls
