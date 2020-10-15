from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound
import markdown2
from markdown2 import Markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    mk = Markdown()
    # ask if title exists
    print(f"LOG title: {title}")
    print(f"LOG util.get_entry(title): {util.get_entry(title)}")
    entry_title = util.get_entry(title)
    if entry_title is None:
        return HttpResponseNotFound(f" The entry with name {title} was not found.")
    else:
        return render(request, "encyclopedia/title.html", {
            "title_content": mk.convert(util.get_entry(title)),
            "title": title
        })

