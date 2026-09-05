from django.shortcuts import render
from .models import Blog

def home(request):
    blogs = Blog.objects.all()
    context = {'blog' : blogs}
    return render(request , 'core/home.html' , context)

def about(request):
    return render(request , 'core/about.html')

def blog(request , pk):
    blog = Blog.objects.get(id = pk)
    context = {'blg' : blog}
    return render(request , 'core/blog.html' , context)