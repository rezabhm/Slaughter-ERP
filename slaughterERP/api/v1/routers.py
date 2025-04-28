from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

# Rest Framework Router
router = DefaultRouter()

# login
# accounts
# role
# contact

urlpatterns = router.urls

# Manual url
urlpatterns += [

    path('auth/login', TokenObtainPairView.as_view(), name='login')

]
