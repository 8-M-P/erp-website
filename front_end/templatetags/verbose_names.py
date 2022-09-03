from django import template

register = template.Library()


@register.simple_tag
def get_verbose_name(obj, field):
    return obj._meta.get_field(field).verbose_name.title()


@register.simple_tag
def get_model_verbose_name(obj):
    return obj._meta.verbose_name_plural.title()
