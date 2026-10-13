from django.shortcuts import render , redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Blog , Topic , Comments , User
from .forms import BlogForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        user = authenticate(request , username=username , password=password)

        if user is not None:
            login(request , user)
            return redirect('home')
        elif not username or not password:
            messages.error(request , 'Invalid Username OR Password')
        else:
            messages.error(request , 'Username OR Password does not exist')
        
    context = {'page' : page}
    return render(request , 'core/login_register.html' , context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request , user)
            return redirect('home')
        else:
            messages.error(request , 'An Error occured during registration')
    
    context = {'page' : page , 'form' : form}
    return render(request , 'core/login_register.html' , context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    blogs = Blog.objects.filter(
        Q(topic__name__icontains=q) |
        Q(title__icontains=q) |
        Q(author__username__icontains=q)
        )
    
    topics = Topic.objects.all()
    blog_count = blogs.count()
    blog_comments = Comments.objects.filter(Q(blog__topic__name__icontains=q))
    
    context = {'blog' : blogs , 'topics' : topics , 
               'blog_count' : blog_count , 
               'blog_comments' : blog_comments}
    return render(request , 'core/home.html' , context)

def about(request):
    return render(request , 'core/about.html')

def blog(request , pk):
    blog = Blog.objects.get(id = pk)
    blog_comments = blog.comments_set.all()
    participants = blog.Participants.all()
    if request.method == "POST":
        comment = Comments.objects.create(
            user = request.user,
            blog = blog,
            body = request.POST.get('body')
        )
        blog.Participants.add(request.user)
        return redirect('blog' , pk = blog.id)
    
    context = {'blg' : blog , 'blog_comments' : blog_comments , 'participants' : participants}
    return render(request , 'core/blog.html' , context)

def userProfile(request , pk):
    user = User.objects.get(id=pk)
    blogs = user.blog_set.all()
    blog_comments = user.comments_set.all()
    topics = Topic.objects.all()
    context = {'user' : user , 'blog' : blogs , 'blog_comments' : blog_comments , 'topics' : topics}
    return render(request , 'core/profile.html' , context)

@login_required(login_url='login')
def createblog(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
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

@login_required(login_url='login')
def deletecomments(request , pk):
    comment = Comments.objects.get(id=pk)
    
    if request.user != comment.user:
            messages.error(request, 'You are not authorized to update this blog.')
            return redirect('home')
    
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request , 'core/delete.html' , {'obj' : comment}) 