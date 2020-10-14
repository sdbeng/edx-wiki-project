from django.shortcuts import render
import markdown2

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    # title
    return render(request, "encyclopedia/title.html", {
        "title_content": markdown2.markdown(util.get_entry(title)), "title": title
    })
