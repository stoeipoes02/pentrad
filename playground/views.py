from django.shortcuts import render, redirect
from django.http import HttpResponse
from playground.models import Person
# Create your views here.
# request -> response
# request handler


def calculate():
    x = 3
    result = x + 2
    return result


def say_hello(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        p = Person(first_name=first_name, last_name=last_name)
        p.save()
        return redirect('/playground/add/')
    x = calculate()
    return render(request, 'add.html', {'name':'Kick', 'var':x})


def show_people(request):
    if request.method == 'POST' and request.POST['action'] == 'delete_last':
        last_person = Person.objects.last()
        if last_person:
            last_person.delete()
    people = Person.objects.all()
    return render(request, 'people.html', {'people': people})

def home(request):
    return render(request, 'home.html')