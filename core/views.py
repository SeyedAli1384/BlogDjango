from django.shortcuts import render , redirect
from django.db.models import Q
from .models import Blog , Topic
from .forms import BlogForm

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    blogs = Blog.objects.filter(
        Q(topic__name__icontains=q) |
        Q(title__icontains=q) |
        Q(author__username__icontains=q)
        )
    
    topics = Topic.objects.all()
    blog_count = blogs.count()
    
    context = {'blog' : blogs , 'topics' : topics , 'blog_count' : blog_count}
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

def updateblog(request , pk):
    blog = Blog.objects.get(id=pk)
    form = BlogForm(instance=blog)
    if request.method == 'POST':
        form = BlogForm(request.POST , instance=blog)
        if form.is_valid():
                    form.save()
                    return redirect('home')
                
    context = {'form' : form}
    return render(request , 'core/blog_form.html' , context)

def deleteblog(request , pk):
    blog = Blog.objects.get(id=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('home')
    return render(request , 'core/delete.html' , {'obj' : blog})