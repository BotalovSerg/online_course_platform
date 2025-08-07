from django.urls import path

from .views import (
    AccessRolesRuleDetailView,
    AccessRolesRuleView,
    BusinessElementDetailView,
    BusinessElementView,
    RoleDetailView,
    RoleView,
)

urlpatterns = [
    path("roles/", RoleView.as_view(), name="roles"),
    path("roles/<int:role_id>/", RoleDetailView.as_view(), name="roles-update"),
    path("elements/", BusinessElementView.as_view(), name="business-element"),
    path(
        "elements/<int:element_id>/",
        BusinessElementDetailView.as_view(),
        name="business-element-update",
    ),
    path("rules/", AccessRolesRuleView.as_view(), name="access-rules"),
    path(
        "rules/<int:rule_id>/",
        AccessRolesRuleDetailView.as_view(),
        name="access-rules-update",
    ),
]
