from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def user_liked(likes, user):
    return likes.filter(user=user)


@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name
