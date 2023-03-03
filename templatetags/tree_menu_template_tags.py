from django import template
from ..models import TreeMenuItem
from django.urls import reverse

register = template.Library()

class Vertex:
    def __init__(self, obj):
        self.id             = obj['id']
        self.name           = obj['public_name']
        self.link           = obj['link']
        self.sort_priority  = obj['sort_priority']
        self.parent         = obj['parent_item']
        self.reverse_link   = obj['reverse_link']
        self.children       = []

@register.inclusion_tag('tree_menu_templates/tree_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    items = TreeMenuItem.objects.values(
        'id', 
        'public_name', 
        'link', 
        'sort_priority', 
        'parent_item', 
        'reverse_link').filter(
        menu__name=menu_name,
    )
    items_list = list(items)
    ids_and_vertices = {}
    vertices = []
    children = {}
    for item in items_list:
        v = Vertex(item)
        vertices.append(v)
        ids_and_vertices[v.id] = v
        if v.parent != None:
            if v.parent in children:
                children[v.parent].append((v.sort_priority, v))
            else:
                children[v.parent] = [(v.sort_priority, v)]
    for id in children:
        ids_and_vertices[id].children = children[id]
    for v in vertices:
        if v.reverse_link:
            v.link = reverse(v.link)
        v.children.sort(key=lambda x: x[0])
    current_item = None
    for v in vertices:
        if v.link == context.request.path:
            current_item = v
            break
    elements = []
    while current_item != None:
        elements.insert(0, current_item.link)
        if current_item.parent:
            current_item = ids_and_vertices[current_item.parent]
        else: 
            current_item = None
    return {'root_nodes': sorted(
                [(v.sort_priority, v) for v in vertices if not v.parent], 
                key=lambda x: x[0]), 
            'opened': elements
            }
    