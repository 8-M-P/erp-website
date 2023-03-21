from django import template

register = template.Library()


@register.filter(name="typecheck")
def isinstance_filter(val, instance_type):
    return isinstance(val, eval(instance_type))


# Only Int value check
@register.filter(name="isequel")
def isequel_filter(val, val2):
    return int(val) == val2


@register.filter(name="isselected")
def is_selected(selected_list, key):
    for x in selected_list:
        if hasattr(x, "pk"):
            if x.pk == key:
                return True
    return False


@register.filter(name="moneyformat")
def money_format(val):
    newval = val.rsplit(",", 1)
    newval[0] = newval[0].replace(".", ",")
    newval = ".".join(newval)
    return "₺" + newval


@register.filter(name="totalformat")
def total_money_format(price, tax_rate):
    # price * (1 + (Number(attr.tax_rate) / 100)
    total = float(price) * (1 + (float(tax_rate) / 100))
    return total


@register.filter(name="commatopoint")
def commatopoint(val):
    return str(val).replace(",", ".")


@register.filter(name="mult")
def mult(value, arg):
    return int(value) * int(arg)


@register.filter(name="sub")
def sub(value, arg):
    return int(value) - int(arg)


@register.filter(name="div")
def div(value, arg):
    return int(value) / int(arg)


# let islem_tutar = price * unit
# let iskonto_tutar = islem_tutar * discount / 100
# let ara_toplam = islem_tutar * (100 - discount) / 100
# let total_price = ara_toplam * (1 + (Number(attr.tax_rate) / 100))
# let kdv_toplam = (total_price - (total_price / (1 + (Number(attr.tax_rate) / 100))))

@register.filter(name="total")
def total(price, unit):
    return round(float(price) * float(unit), 2)


@register.simple_tag
def discount_sum(price, unit, discount):
    total = float(price) * float(unit)
    return round(total * float(discount) / 100, 2)


@register.simple_tag
def sub_total(price, unit, discount):
    total = float(price) * float(unit)
    return round(total * (100 - float(discount)) / 100, 2)


@register.simple_tag
def final_total(price, unit, discount, tax_rate):
    total = float(price) * float(unit)
    sub_total = total * (100 - float(discount)) / 100
    return round(sub_total * (1 + (float(tax_rate) / 100)), 2)


@register.simple_tag
def vat_total(price, unit, discount, tax_rate):
    total = float(price) * float(unit)
    sub_total = total * (100 - float(discount)) / 100
    total_price = sub_total * (1 + (float(tax_rate) / 100))
    return round(total_price - (total_price / (1 + (float(tax_rate) / 100))), 2)
