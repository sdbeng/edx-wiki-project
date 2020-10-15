from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound
import markdown2

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    # ask if title exists
    # print(f"LOG title: {title}")
    if util.list_entries() == None:
        return HttpResponseNotFound(f" The entry with name {title} was not found.")
    return render(request, "encyclopedia/title.html", {
        "title_content": markdown2.markdown(util.get_entry(title)), "title": title
    })

