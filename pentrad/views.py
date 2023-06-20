from django.shortcuts import render

def homepage_view(request):
    # Your code to render the homepage goes here
    return render(request, 'home.html')
