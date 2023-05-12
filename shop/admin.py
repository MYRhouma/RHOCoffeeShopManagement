from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from shop.models import Account, Business, Product, Category, Menu, OrderItem, Order, Customer, Table


# Register your models here.

class BusinessAdmin(admin.ModelAdmin):
    list_display = ("name", "type","country")
admin.site.register(Business,BusinessAdmin)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Table)
admin.site.register(OrderItem)
admin.site.register(Customer)
@admin.register(Account)
class UserAdmin(admin.ModelAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    # change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("business","type","username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone_number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "email", "phone_number","first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email","phone_number")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )