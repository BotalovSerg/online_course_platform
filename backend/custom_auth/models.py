import bcrypt

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        password=None,
        patronymic="",
        role=None,
    ):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, patronymic=""):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            password=password,
            role=None,  # Для суперюзера роль не нужна, так как это для Django Admin
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role = models.ForeignKey("custom_rbac.Role", on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def set_password(self, raw_password):

        if raw_password:
            self.password = bcrypt.hashpw(
                raw_password.encode("utf-8"),
                bcrypt.gensalt(),
            ).decode("utf-8")

    def check_password(self, raw_password):

        return bcrypt.checkpw(raw_password.encode("utf-8"), self.password.encode("utf-8"))

    class Meta:
        db_table = "users_user"
