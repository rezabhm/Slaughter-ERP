"""
URL configuration for configs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from graphene_django.views import GraphQLView
from rest_framework import permissions

from graphql.schema import schema

schema_view = get_schema_view(

    openapi.Info(
        title="Slaughter ERP Buy and Orders Service",
        default_version='v1',
        description="api docs for Slaughter ERP Buy and Orders \n base url : api/v1/ ",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],

)

from apps.core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthz/', core_views.healthz, name='healthz'),

    # documentation
    path('api-docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-docs/re-doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API version 1
    path('api/v1/', include('api.v1.routers')),

    # GraphQL endpoint
    path("graph-ql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
