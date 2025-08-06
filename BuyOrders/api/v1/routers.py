from api.v1.buy.production_order.view import ProductionOrderAPIView
from api.v1.order.bank_account.view import BankAccountAPIView
from api.v1.order.invoice.view import InvoiceAPIView
from api.v1.order.payment.view import PaymentAPIView
from api.v1.order.purchase_order.view import PurchaseOrderAPIView
from utils.CustomRouter.CustomRouter import CustomRouter

router = CustomRouter()

router.register('buy-product', ProductionOrderAPIView)
router.register('order-bank-account', BankAccountAPIView)
router.register('order-invoice', InvoiceAPIView)
router.register('order-payment', PaymentAPIView)
router.register('order-purchase-order', PurchaseOrderAPIView)

urlpatterns = router.urls
