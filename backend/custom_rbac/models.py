from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "auth_role"


class BusinessElement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "auth_businesselement"


class AccessRolesRule(models.Model):
    role = models.ForeignKey("Role", on_delete=models.CASCADE)
    element = models.ForeignKey("BusinessElement", on_delete=models.CASCADE)
    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.role.name} - {self.element.name}"

    class Meta:
        db_table = "auth_accessrolesrule"
        unique_together = ("role", "element")
