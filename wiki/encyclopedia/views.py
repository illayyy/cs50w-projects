import markdown2 as md
import random as rand

from django.shortcuts import render, redirect

from . import util


def index(request):
    msg = ""
    header = "All Pages"
    entries = util.list_entries()

    if not entries:
        msg = "No entries found."

    return render(request, "encyclopedia/index.html", {
        "header": header,
        "entries": entries,
        "msg": msg
    })


def search(request):
    msg = ""
    header = "Search Results"

    q = request.GET['q']
    found_entries = []
    for e in util.list_entries():
        if q.lower() in e.lower():
            if q.lower() == e.lower():
                return redirect('entry', e)
            found_entries.append(e)

    if not found_entries:
        msg = "No entries found."

    return render(request, "encyclopedia/index.html", {
        "header": header,
        "entries": found_entries,
        "msg": msg
    })


def entry(request, title):
    content = util.get_entry(title)
    if content is not None:
        content = md.markdown(content)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })

    return render(request, "encyclopedia/pagenotfound.html", {
        "title": title
    })


def new(request):
    msg = ""
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if not title:
            msg = f"Title cannot be empty."
        elif title.lower() in [e.lower() for e in util.list_entries()]:
            msg = f"The page <a href='{title}'><i>{title}</i></a> already exists."
        else:
            util.save_entry(title, content)
            return redirect('entry', title)

    return render(request, "encyclopedia/new.html", {
        "msg": msg
    })


def edit(request, title):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect('entry', title)

    content = util.get_entry(title)
    if content is not None:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

    return render(request, "encyclopedia/pagenotfound.html", {
        "title": title
    })


def random(request):
    entries = util.list_entries()
    random_entry = rand.choice(entries)
    return redirect('entry', random_entry)
