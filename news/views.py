from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.conf import settings
from datetime import datetime
import json


# Create your views here.
class MainPageView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        with open(settings.NEWS_JSON_PATH, "r") as json_file:
            news_from_json = json.load(json_file)
            dates = []
            articles = []
            for article in news_from_json:
                if q in article['title']:
                    articles.append(article)
                    date = article["created"].split(" ")[0]
                    article["date"] = date
                    if date not in dates:
                        dates.append(date)
            return render(request, 'news/newshome.html',
                          context={'news': articles, 'dates': sorted(dates, reverse=True)})


class ArticleView(TemplateView):
    template_name = "news/news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with open(settings.NEWS_JSON_PATH, "r") as json_file:
            news_from_json = json.load(json_file)
            art_link = int(kwargs['link'])
            art = [n for n in news_from_json if n["link"] == art_link][0]
            context['title'] = art["title"]
            context['text'] = art["text"]
            context['created'] = art['created']
            return context


class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class CreateNewsView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, "r") as json_file:
            news_from_json = json.load(json_file)

            news_from_json.append({
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'text': request.POST.get('text'),
                'title': request.POST.get('title'),
                'link': max([int(art['link']) for art in news_from_json]) + 1})

        with open(settings.NEWS_JSON_PATH, 'w') as f:
            json.dump(news_from_json, f)

        return redirect('/news/')
