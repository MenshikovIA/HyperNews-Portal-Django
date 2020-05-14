from django import template
register = template.Library()


@register.filter
def get_item(dic, key):
    return dic.get(key)

@register.filter
def get_news_by_date(news, date):
    return [art for art in news if art["date"] == date]
