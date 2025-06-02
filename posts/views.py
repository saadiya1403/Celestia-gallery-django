import json
from urllib import request
from .models import Post, Like
from .forms import PostForm  # new
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework import serializers
from django.db.models import Prefetch, Exists, OuterRef
from django.shortcuts import render

def HomePageView(request):
    if request.user.is_authenticated:
        LikesByUser = Like.objects.filter(user=request.user)
    else:
        LikesByUser = None
    context = { 
        'posts' : Post.objects.all(),
        'LikesByUser' : LikesByUser
    }
    return render(request, 'home.html', context)

@login_required(login_url='/accounts/login/') 
def CreatePost(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            form = PostForm()
        return redirect('home')
    
    return render(request, 'post.html', {'form': form})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'post_detail.html', {'post': post})

@csrf_exempt
def add_like(request):
    if request.method == 'POST':
        jsonResponse = json.loads(request.body.decode('utf-8'))
        _user_id = jsonResponse['user_id']
        _post_id = jsonResponse['post_id']
        
        _User = User.objects.get(id=_user_id)
        _Post = Post.objects.get(id=_post_id)
        NewLike = Like()
        NewLike.user = _User
        NewLike.post = _Post
        NewLike.save()
        _Post.Like_Count +=1
        _Post.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

def color_palette():  # Defining the view function
    return redirect('http://127.0.0.1:5000')  # Redirecting to the specified URL
