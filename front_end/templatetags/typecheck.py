from django import template

register = template.Library()


@register.filter(name="typecheck")
def isinstance_filter(val, instance_type):
    return isinstance(val, eval(instance_type))


@register.filter(name="isselected")
def is_selected(selected_list, key):
    return any(x.pk == key for x in selected_list)
