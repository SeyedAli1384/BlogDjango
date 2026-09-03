from django.shortcuts import render

blogs = [
    {'id' : 1 , 'name' : 'Learn x with y'},
    {'id' : 2 , 'name' : 'How x live in y situation'},
    {'id' : 3 , 'name' : 'What x do and its benefits'},
]

def home(request):
    context = {'blog' : blogs}
    return render(request , 'core/home.html' , context)

def about(request):
    return render(request , 'core/about.html')

def blog(request , pk):
    blog = None
    for i in blogs:
        if i['id'] == int(pk):
            blog = i    
    context = {'blg' : blog}
    return render(request , 'core/blog.html' , context)