from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# request -> response
# request handler


def calculate():
    x = 3
    result = x + 2
    return result


def say_hello(request):
    x = calculate()
    return render(request, 'hello.html', {'name':'Kick', 'var':x})