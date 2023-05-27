from django import template

register = template.Library()


@register.filter
def add_class(value, css_class):
    attrs = value.field.widget.attrs
    attrs['class'] = css_class
    return value
