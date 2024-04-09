from django.contrib import admin
from django.utils.html import format_html

from tree_menu.models import Item
from tree_menu.models import Menu


@admin.register(Item)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "parent", "slug", "item_url")
    list_filter = ("menu",)
    fieldsets = (
        (
            "Add or edit item",
            {"fields": (("menu", "parent"), "title", "slug")},
        ),
    )

    def item_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.url)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
