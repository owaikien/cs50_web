from django.shortcuts import render

from . import util
from markdown2 import Markdown
import random

def markdown_to_html(title):
    markdowner = Markdown()
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = markdown_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This page does not exist!"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "message": html_content
        })
    
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = markdown_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                'title': entry_search,
                'message': html_content
            })
        else:
            allEntries = util.list_entries()
            recommendations = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendations.append(entry)
            return render(request, "encyclopedia/search.html", {
                    'recommendation': recommendations
            })
        
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        TitleExist = util.get_entry(title)
        if TitleExist is not None:
            return render(request, "encyclopedia/error.html", {
                'message': "This title has already existed!"
            })
        else:
            util.save_entry(title, content)
            html_content = markdown_to_html(title)
            return render(request, 'encyclopedia/entry.html', {
                'title': title,
                'message': html_content
            })
        
def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title, 
            "content": content
        })
    
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = markdown_to_html(title)
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'message': html_content
        })
    
def rand(request):
    allEntries = util.list_entries()
    title = random.choice(allEntries)
    html_content = markdown_to_html(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "message": html_content
    })