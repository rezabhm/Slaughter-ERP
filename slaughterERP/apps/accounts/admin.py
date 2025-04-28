from django.contrib import admin

from apps.accounts.models import *

# Register your models here.
admin.site.register(Role)
admin.site.register(CustomUser)
admin.site.register(Contact)
