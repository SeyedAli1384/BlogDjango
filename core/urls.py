from django.urls import path
from . import views

urlpatterns = [
    path('login/' , views.loginPage , name='login'),
    path('logout/' , views.logoutUser , name='logout'),
    path('' , views.home , name="home"),
    path('about/' , views.about , name="about"),
    path('blog/<str:pk>/' , views.blog , name="blog"),
    path('create-blog/' , views.createblog , name="create-blog"),
    path('update-blog/<str:pk>/' , views.updateblog , name="update-blog"),
    path('delete-blog/<str:pk>/' , views.deleteblog , name="delete-blog"),
]
