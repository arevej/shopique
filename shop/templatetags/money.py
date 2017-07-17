from django import template
register = template.Library()

def format_money(value):
    return '$' + format("%.2f" % value)

register.filter('format_money', format_money)
