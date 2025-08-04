from django.contrib import admin
from .models import Role, BusinessElement, AccessRolesRule


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    pass


@admin.register(AccessRolesRule)
class AccessRolesRuleAdmin(admin.ModelAdmin):
    pass
