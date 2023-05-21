from django import template

register = template.Library()

@register.filter
def index(df, index_value):
    index_value = int(index_value)
    print(index_value)
    pb = df.iloc[index_value]
    return pb