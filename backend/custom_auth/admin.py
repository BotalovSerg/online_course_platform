from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):

    def save_model(
        self,
        request: HttpRequest,
        obj: CustomUser,
        form: ModelForm,
        change: bool,
    ) -> None:
        super().save_model(request, obj, form, change)

        obj.set_password(obj.password)
        obj.save()
