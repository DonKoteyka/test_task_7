from django import template
from django.utils.datastructures import MultiValueDictKeyError

from tree_menu.models import Item

register = template.Library()


@register.inclusion_tag("nested_menu.html", takes_context=True)
def draw_menu(context: template.Context, menu_name: str) -> dict:
    """
    function takes context of a draw_menu call and a name of menu to draw and
    collects a data dict for rendering nested menu
    It collects recursively all parent menu items to the active item and directly
    connected child menu items
    :param context: the context in which the menu is being rendered.
    :param menu_name: the title of the menu that is being rendered
    :return: result_dict: A dictionary containing the primary items of the menu
    and child items that have been selected.
    """
    items = Item.objects.select_related("menu").filter(menu__title=menu_name)
    items_listed = list(items.values())
    items_id_dict = {item["id"]: item for item in items_listed}
    primary_items = [item for item in items_listed if item.get("parent_id") is None]

    try:
        selected_item_id = int(context["request"].GET[menu_name])
    except MultiValueDictKeyError:
        pass  # on start page we need only primary_items so this exception can be passed for DRY reasons
    else:
        selected_item_id_list = get_selected_item_id_list(items_id_dict, primary_items, selected_item_id)

        for item in primary_items:
            if item["id"] in selected_item_id_list:
                item["child_items"] = get_child_items(items_listed, item["id"], selected_item_id_list)

    result_dict = {"items": primary_items, "menu": menu_name, "other_querystring": get_querystring(context, menu_name)}
    return result_dict


def get_querystring(context: template.Context, menu_name: str) -> str:
    """
    This function takes in two arguments, context and menu_name, and returns
    a string that represents the query string from the request that was not
    used to select the current item.
    :param context: the context in which the menu is being rendered.
    :param menu_name: the title of the menu that is being rendered
    :return: the querystring from the request that was not used to select the current item
    """
    querystring_args = []
    for key in context["request"].GET:
        if key != menu_name:
            querystring_args.append(key + "=" + context["request"].GET[key])
    return "&".join(querystring_args)


def get_child_items(items_values: list[dict], current_item_id: int, selected_item_id_list: list[int]) -> list[dict]:
    """
    This function takes in three arguments: items_values, current_item_id, and
    selected_item_id_list. It returns a list of all child items that belong
    to the item with the current_item_id.
    :param items_values: list of dictionaries that represents all the items in the menu
    :param current_item_id: the id of the current item for which to retrieve child items
    :param selected_item_id_list: a list of ids for items that have been selected in the menu
    :return: a list of items with same parent as selected item and child items for selected items
    """
    item_list = [item for item in items_values if item.get("parent_id") == current_item_id]
    for item in item_list:
        if item["id"] in selected_item_id_list:
            item["child_items"] = get_child_items(items_values, item["id"], selected_item_id_list)
    return item_list


def get_selected_item_id_list(
    items_id_dict: dict[int, dict], primary_items: list[dict], selected_item_id: int
) -> list[int]:
    """
    This function takes in three arguments: items_id_dict, primary_item, and selected_item_id.
    It returns a list of ids for all the items that have been selected in the menu so far.
    :param items_id_dict: dictionary that maps the id of an item to the item's dictionary representation
    :param primary_items: a list of dictionaries that represent the items that have no parent item
    :param selected_item_id: the id of the item that was selected in the rendered menu
    :return: list of ids of items starting with the most recently selected item and working
    up the chain of parent items
    """
    selected_item_id_list = []
    parent_id = items_id_dict[selected_item_id]["id"]

    while parent_id:
        selected_item_id_list.append(parent_id)
        parent_id = items_id_dict[parent_id].get("parent_id")
    if not selected_item_id_list:
        for item in primary_items:
            if item["id"] == selected_item_id:
                selected_item_id_list.append(selected_item_id)
    return selected_item_id_list
