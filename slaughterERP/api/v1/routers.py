from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.accounts.contact_view import ContactAdminAPIView, ContactAPIView
from api.v1.accounts.role_view import AdminRoleAPIView
from api.v1.accounts.users_view import UsersAdminAPIView, UsersAPIView

# Rest Framework Router
router = DefaultRouter()

# login
# accounts
router.register('accounts/a/users', UsersAdminAPIView, basename='admin-users')
router.register('accounts/r/users', UsersAPIView, basename='users')
router.register('accounts/a/role', AdminRoleAPIView, basename='admin-role')
router.register('accounts/a/contact', ContactAdminAPIView, basename='admin-contact')
router.register('accounts/r/contact', ContactAPIView, basename='contact')

# role
# contact

urlpatterns = router.urls

# Manual url
urlpatterns += [

    path('auth/login', TokenObtainPairView.as_view(), name='login')

]
