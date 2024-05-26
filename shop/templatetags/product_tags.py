from django import template

register = template.Library()

@register.inclusion_tag('shop/product_item.html')
def render_product(product):
    return {'product': product}