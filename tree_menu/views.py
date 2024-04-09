from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import TemplateView

from tree_menu import models


class IndexPageView(TemplateView):
    template_name = "index.html"


def slug_view(request, item_slug):
    menu_item = get_object_or_404(models.Item, slug=item_slug)
    return redirect(menu_item.url)
