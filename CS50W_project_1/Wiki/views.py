from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import random
from django.shortcuts import redirect
from django.utils.safestring import mark_safe

# Create your views here.
pages = {'CSS': 'CSS stands for Cascading Style Sheets',
         
         'HTML': "HTML stands for Hyper Text Markup Language",

         'Javascript': "JavaScript is a dynamic programming language that's used for web development",

         'Django': 'Python-based web framework simplifying web development via clean design, rapid development, and powerful features for scalable, secure applications.',

         'Python': 'High-level, versatile programming language known for readability, ease, extensive libraries, and  applicability in various domains, from web to AI.',

         'Swift': "Swift is a powerful and modern programming language developed by Apple for building applications on iOS, macOS, watchOS, and tvOS. Introduced in 2014, Swift was designed to be fast, safe, and expressive. It combines elements from various programming languages and is known for its readability and ease of use. Swift incorporates modern features like type inference, optionals for handling nil values, closures, and protocols, enabling developers to write more reliable and efficient code. It's continually evolving, with an open-source community contributing to its growth and improvement. Swift offers a robust alternative to Objective-C, providing a streamlined and versatile language for Apple ecosystem development.",

         'SwiftUI': "Declarative framework for building user interfaces in Swift, enabling efficient, interactive, and platform-agnostic app development across Apple devices.",

         'OBJ-C': "Primary programming language for Apple's macOS and iOS, predecessor to Swift, known for its dynamic runtime and extensive libraries."
         }

class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Name", widget=forms.TextInput(attrs={'id': 'new-page-title'}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'id': 'new-page-desc'}))
    
def home(request):
    return render(request, "Wiki/home.html", {
        "pages": pages
    })

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        lowercase_array = [x.lower() for x in pages.keys()]
        new_title = form.data.get('title')
        if new_title.lower() in lowercase_array:
            error_msg = f'Already have article with name <strong>{new_title.upper()}</strong>'
            form.add_error('title', mark_safe(error_msg))
        if form.is_valid():
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["description"]
            if title not in pages.keys():
                pages[title] = desc
                return redirect('wiki:details', title)
        else:
            return render(request, "Wiki/create_new_page.html", {
                "form": form
            })

    return render(request, "Wiki/create_new_page.html", {
        "form": NewPageForm(),
        "is_edit": False
    })

def page_details(request, element):
    if element in pages.keys():
        value = pages[element]
        dict = {
                    element:value
                }
        return render(request, "Wiki/page_details.html", {
            "element": dict
        })
    else:
        return render(request, "Wiki/no_pages.html", {"element" : element})

def open_random_page(request):
    if pages:
        random_key = random.choice(list(pages.keys()))
        return redirect('wiki:details', random_key)
    else:
        return HttpResponse("No pages left")

def delete_page(request, element):
    if element in pages.keys():
        del pages[element]
        return HttpResponseRedirect(reverse('wiki:home'))
    else:
        return render(request, "Wiki/no_pages.html", {"element": element})

def edit_page(request, element):
    if request.method == "GET":
        if element in pages:
            initial_data = {'title': element,
                            'description': pages[element]
                            }
            form = NewPageForm(initial=initial_data)
            return render(request, "Wiki/create_new_page.html", {
                    "form": form,
                    "is_edit": True
                })
        else:
            # Page not found, redirect to a specific page or handle as needed
            return render(request, "Wiki/no_pages.html", {"element": element})
    else:
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["description"]
            if title in pages.keys():
                pages[title] = desc
                return redirect('wiki:details', title)
            else:
                if element in pages.keys():
                    del pages[element]
                    pages[title] = desc
                    return redirect('wiki:details', title)
    return render(request, "Wiki/no_pages.html", {"element": element})       
     
def search_view(request):
    query = request.GET.get('q')

    if query:
        lower_query = str(query.lower())
        filtered_dict = {key: value for key, value in pages.items() if lower_query in key.lower() or lower_query in value.lower()}
        return render(request, "Wiki/home.html", {
        "pages": filtered_dict,
        "query": query
    })
    else:
        return HttpResponse("Fill the search field")
                