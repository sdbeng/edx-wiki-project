from django.shortcuts import render
from django import forms
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
import markdown2
from markdown2 import Markdown
from django.urls import reverse

from . import util
# ot use forms create class
class NewTitleForm(forms.Form):
    title=forms.CharField(label="New Title")
    content=forms.CharField(widget=forms.Textarea(attrs={
        'cols':20, 'rows':5},))

def index(request):
    print(util.list_entries())
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    mk = Markdown()
    # ask if title exists
    print(f"LOG title: {title}")
    # print(f"LOG util.get_entry(title): {util.get_entry(title)}")
    entry_title = util.get_entry(title)
    if entry_title is None:
        return HttpResponseNotFound(f" The entry with name {title} was not found.")
    else:
        return render(request, "encyclopedia/title.html", {
            "title_content": mk.convert(util.get_entry(title)),
            "title": title
        })

def search(request):
    querySearch = request.GET.get('q', '') # q is the str name in the url and in the input tag
    print(f"query: {querySearch}")
    entries_list = util.list_entries()
    print(f"entries_list {entries_list}")
    new_list = []
    if querySearch is not None:
        return HttpResponseRedirect("/")
        # return HttpResponseRedirect(reverse("wiki"), kwargs={'title': querySearch})
    else:
        for entry in entries_list:
            if querySearch in entry:
                new_list.append(entry)
            
        return render(request, "encyclopedia/index.html", {
            "new_list": new_list,
            "search": True,
            "querySearch": querySearch
        })

def add(request):
    if request.method == "POST":
        # save new data entry in the form var
        form = NewTitleForm(request.POST)
        # then do server-side validation
        if form.is_valid():
            # if title is valid, save it
            # Note1: ["title"] is the class title field prop
            # Note2: ["content"] is the class content field prop
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # then add the title and content to the list
            # todo: check if title already exists, show message, otherwise save it w/ save_entry(title, content)
            all_titles = util.list_entries()
            for filename in all_titles:
                if title.lower() == filename.lower():
                    return HttpResponse('This title already exists.')
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('index'))
        else:
            # if data is not clean, pass form back out
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    # otherwise if it's not a post return a blank form
    return render(request, 'encyclopedia/add.html', {
        "form": NewTitleForm()
    })