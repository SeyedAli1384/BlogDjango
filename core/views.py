from django.shortcuts import render , redirect
from .models import Blog
from .forms import BlogForm

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

def createblog(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form' : form}
    return render(request , 'core/blog_form.html' , context)