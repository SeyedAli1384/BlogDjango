from django.shortcuts import render
from .models import Blog

def home(request):
    blogs = Blog.objects.all()
    context = {'blog' : blogs}
    return render(request , 'core/home.html' , context)

def about(request):
    return render(request , 'core/about.html')

def blog(request , pk):
    blogs = Blog.objects.all()
    for i in blogs:
        if i.author == str(pk):
            blog = i    
    context = {'blg' : blog}
    return render(request , 'core/blog.html' , context)