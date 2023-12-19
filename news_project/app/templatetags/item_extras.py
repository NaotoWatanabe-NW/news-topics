from django import template

register = template.Library()

@register.simple_tag
def url_replace(request, Field, value):
    dict_ = request.GET.copy()
    dict_[Field] = value
    return dict_.urlencode()
