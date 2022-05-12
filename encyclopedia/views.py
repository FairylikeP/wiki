from http.client import HTTPResponse
from tkinter.tix import Form
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms
from random import choice
import re
from . import util
from markdown2 import Markdown

class NewEntryForm(forms.Form):
    name = forms.CharField(label = "Title", max_length = 100, widget= forms.TextInput(attrs={'placeholder': "Entry's title", 'class': "form-control"}))
    entry = forms.CharField(label = "", widget = forms.Textarea(attrs={'placeholder':"Write the content here", 'rows':"18", 'class': "form-control"}))
class EditForm(forms.Form):
    entry = forms.CharField(label = "Content", widget = forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def edit(request, title):
    if request.method == "POST":
        # Once the user submits the edits we check if the form data is valid
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['entry']
            util.save_entry(title, content)
            # Once the entry is saved, the user should be redirected back to that entry’s page.
            return HttpResponseRedirect(reverse("wikiPage", args=(title, )))
        else:
            # If the form is not valid then the user should be taken back to the editing page with an error
            return render(request, "encyclopedia/edit.html", {
            "form": form    
            })
    else:
        if util.get_entry(title):
            # If the method is get then the user will be taken to the text editor page
            initial = {"entry" : util.get_entry(title)}
            # The textarea should be pre-populated with the existing Markdown content of the page. 
            formInitial = EditForm(initial=initial)
            return render(request, "encyclopedia/edit.html", {"form": formInitial, "title":title})
        else:
            # The entry doesn't exist so the user will be shown an error
            return render(request, "encyclopedia/noentry.html", {"title": title})

def search(request):
   if request.method == "POST":
        # The entry that the person searched for
        searched = request.POST['q']
        entries = util.list_entries()
        # If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page. 
        if util.get_entry(searched):
            markdowner = Markdown()
            content = markdowner.convert(util.get_entry(searched))
            return render(request, "encyclopedia/title.html" , {"entry": content , "title": searched})
        else:
            # we make a list of all the entries that contain the query
            matched = []
            for item in entries:
                # If the entry contains the searched query
                regexItem = ".*" + re.escape(searched) + ".*"
                if re.search(regexItem, item, re.IGNORECASE):
                    matched.append(item)
            if not len(matched) == 0:
                return render(request, "encyclopedia/results.html", {"matched": matched, "searched": searched})
            # If there was no entry that contained the search query
            else:
                return render(request, "encyclopedia/noentry.html", {"title": searched})
 
def new(request):
    if request.method == "POST":
        #content = request.POST['entry']
        form = NewEntryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            content = form.cleaned_data['entry']
            if util.get_entry(name):
                # Error message that the entry already exists
                form.add_error("name", "Entry already exists!")
                return render(request, "encyclopedia/new.html", {
                    "form": form
                })
            else:
                util.save_entry(name, content)
                return HttpResponseRedirect(reverse("wikiPage", args=(name, )))
    else:
        return render(request, "encyclopedia/new.html", {"form": NewEntryForm()
        })

def random(request):
    entries = util.list_entries()
    randomEntry = choice(entries)
    return HttpResponseRedirect(reverse("wikiPage", args=(randomEntry, )))

def entryPage(request, title):
          
    entry = util.get_entry(title)
    if entry:
        markdowner = Markdown()
        return render(request, "encyclopedia/title.html" , {"entry": markdowner.convert(entry), "title": title})
    else:
        return render(request, "encyclopedia/noentry.html", {"title": title})
