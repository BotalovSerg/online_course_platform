from django.contrib import admin

from .models import AccessRolesRule, BusinessElement, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    pass


@admin.register(AccessRolesRule)
class AccessRolesRuleAdmin(admin.ModelAdmin):
    pass
