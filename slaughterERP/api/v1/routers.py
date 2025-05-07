from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.accounts.contact_view import ContactAdminAPIView, ContactAPIView
from api.v1.accounts.role_view import AdminRoleAPIView
from api.v1.accounts.users_view import UsersAdminAPIView, UsersAPIView
from api.v1.core_ownership.agriculture_view import AgricultureAPIView, AgricultureAdminAPIView
from api.v1.core_ownership.city_view import CityAdminAPIView, CityAPIView
from api.v1.core_ownership.product_owner_view import ProductOwnerAdminAPIView, ProductOwnerAPIView
from api.v1.core_transportation.car_view import CarAdminAPIView, CarAPIView
from api.v1.core_transportation.driver_view import DriverAdminAPIView, DriverAPIView
from api.v1.jwt import CustomTokenObtainPairView
from api.v1.product.product_category_view import ProductCategoryAdminAPIView, ProductCategoryAPIView
from api.v1.product.product_view import ProductAdminAPIView, ProductAPIView
from api.v1.product.unit_view import UnitAdminAPIView, UnitAPIView

# Rest Framework Router
router = DefaultRouter()

# accounts
router.register('admin/accounts/users', UsersAdminAPIView, basename='admin-users')
router.register('any/accounts/users', UsersAPIView, basename='users')
router.register('admin/accounts/role', AdminRoleAPIView, basename='admin-role')
router.register('admin/accounts/contact', ContactAdminAPIView, basename='admin-contact')
router.register('any/accounts/contact', ContactAPIView, basename='contact')

# core.ownership
router.register('admin/ownership/city', CityAdminAPIView, basename='admin-city')
router.register('any/ownership/city', CityAPIView, basename='city')
router.register('admin/ownership/agriculture', AgricultureAdminAPIView, basename='admin-agriculture')
router.register('any/ownership/agriculture', AgricultureAPIView, basename='agriculture')
router.register('admin/ownership/product-owner', ProductOwnerAdminAPIView, basename='admin-product-owner')
router.register('any/ownership/product-owner', ProductOwnerAPIView, basename='product-owner')

# core.transportation
router.register('admin/transportation/driver', DriverAdminAPIView, basename='admin-driver')
router.register('any/transportation/driver', DriverAPIView, basename='driver')
router.register('admin/transportation/car', CarAdminAPIView, basename='admin-car')
router.register('any/transportation/car', CarAPIView, basename='car')

# product
router.register('admin/product/product', ProductAdminAPIView, basename='admin-product')
router.register('any/product/product', ProductAPIView, basename='product')
router.register('admin/product/unit', UnitAdminAPIView, basename='admin-unit')
router.register('any/product/unit', UnitAPIView, basename='unit')
router.register('admin/product/product-category', ProductCategoryAdminAPIView, basename='admin-product-category')
router.register('any/product/product-category', ProductCategoryAPIView, basename='product-category')

urlpatterns = router.urls

# Manual url
urlpatterns += [

    path('auth/login', CustomTokenObtainPairView.as_view(), name='login')

]
