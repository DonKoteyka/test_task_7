from django.urls import path

from tree_menu.views import IndexPageView
from tree_menu.views import slug_view

app_name = "menu"

urlpatterns = [
    path(f"{app_name}/", IndexPageView.as_view(), name="index"),
    path(f"{app_name}/<slug:item_slug>/", slug_view, name="index-detail"),
]
