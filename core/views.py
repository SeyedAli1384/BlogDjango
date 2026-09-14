from django.shortcuts import render , redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from .models import Blog , Topic
from .forms import BlogForm

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request , user)
            return redirect('home')
        elif not username or not password:
            messages.error(request , 'Invalid Username OR Password')
        else:
            messages.error(request , 'Username OR Password does not exist')
        
    context = {}
    return render(request , 'core/login_register.html' , context)

def logoutUser(request):
    logout(request)
    return redirect('home')

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

@login_required(login_url='login')
def createblog(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form' : form}
    return render(request , 'core/blog_form.html' , context)

@login_required(login_url='login')
def updateblog(request , pk):
    blog = Blog.objects.get(id=pk)
    form = BlogForm(instance=blog)
    
    if request.user != blog.author:
        messages.error(request, 'You are not authorized to update this blog.')
        return redirect('home')
    
    if request.method == 'POST':
        form = BlogForm(request.POST , instance=blog)
        if form.is_valid():
                    form.save()
                    return redirect('home')
                
    context = {'form' : form}
    return render(request , 'core/blog_form.html' , context)

@login_required(login_url='login')
def deleteblog(request , pk):
    blog = Blog.objects.get(id=pk)
    
    if request.user != blog.author:
            messages.error(request, 'You are not authorized to update this blog.')
            return redirect('home')
    
    if request.method == 'POST':
        blog.delete()
        return redirect('home')
    return render(request , 'core/delete.html' , {'obj' : blog})