from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *

# Create your views here.
def home(request):
  blogs = Blog.objects.all()
  context = {'blogs':blogs}
  return render(request, "home.html", context)

def displayProfile(request, id):
  print("I am in displayProfile D-Bug")
  user = User.objects.get(id=id)
  followers_ids = Follow.objects.filter(following=user).values_list('follower__id', flat=True)
  followers_user = User.objects.filter(id__in=followers_ids)
  followings_ids = Follow.objects.filter(follower=user).values_list('following__id', flat=True)
  followings_user = User.objects.filter(id__in=followings_ids)
  user_blogs = Blog.objects.filter(author=user)
  is_following = False
  if request.user.is_authenticated:
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
  print(is_following)
  context = {
    'user':user,
    'followers':followers_user,
    'followings':followings_user,
    'blogs':user_blogs,
    'followers_count':followers_user.count(),
    'following_count':followings_user.count(),
    'is_following':is_following
  }
  return render(request, "profile.html", context)

def about(request):
  return render(request, "about.html")

def registerUser(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    password = request.POST.get('password')
    email = request.POST.get('email')

    user = User.objects.filter(username = username)

    if user.exists():
      messages.info(request, "Username Already Exist")
      return redirect("/register")

    user = User.objects.create(
      username = username,
      first_name = first_name,
      last_name = last_name,
      email = email,
    )
    user.set_password(password)
    user.save()
    messages.info(request, "User Created Successfully")
  return render(request, "register.html")

def loginUser(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not User.objects.filter(username=username).exists():
      messages.info(request, "Username Invalid Please Try Again")
      return redirect('/login')
    
    user = authenticate(username=username, password=password)
    if user is None:
      messages.info(request, "Invalid User")
      return redirect('/login')
    else:
      login(request, user)
      return redirect('/')
  return render(request, "login.html")

def logoutUser(request):
  logout(request)
  return redirect('/login')

@login_required(login_url="/login")
def createBlog(request):
  if request.method == 'POST':
    title = request.POST.get('title')
    content = request.POST.get('content')
    blog_image = request.FILES.get('blog_image')
  
    Blog.objects.create(
      title = title,
      content = content,
      author = request.user,
      blog_image = blog_image
    )
    messages.info(request, "Blog Created Success fully")
    return redirect("/createBlog")
  return render(request, "createBlog.html")

@login_required(login_url="/login")
def displayBlog(request, id):
  blog = Blog.objects.get(id = id)
  comments = blog.comments.all() # here we write comments because in django we use related name to access the data of related field
  # blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
  context = {
    'blog':blog,
    'comments':comments
    }
  return render(request, "displayblog.html", context)

def testingRequirement(request):
  user = User.objects.all()
  context = {'user':user}
  return render(request, "testingPage.html", context)

def followToUser(request, id):
  print("I come here in follow to user")
  follow_to_user = get_object_or_404(User, id=id)
  current_user = request.user
  if current_user != follow_to_user:
    if not Follow.objects.filter(follower=current_user, following=follow_to_user).exists():
      Follow.objects.create(follower=current_user, following=follow_to_user)
    return redirect('/profile/{}/'.format(id))
  return redirect('/profile/{}/'.format(id))

def likeToBlog(request, id):
  blog = Blog.objects.get(id = id)
  print("Hellow From like count")
  blog.like_count = blog.like_count + 1
  blog.save()
  return redirect(reverse('displayBlog', args=[blog.id]))

@login_required(login_url="/login")
def commentToBlog(request, id):
  blog = Blog.objects.get(id=id)
  if request.method == 'POST':
    comment_content = request.POST.get('comment')
    if comment_content:
      Comment.objects.create(
        blog=blog,
        user=request.user,
        comment=comment_content
      )
      messages.info(request, "Comment created successfully")
      return redirect(reverse('displayBlog', args=[blog.id]))
  return redirect('/')


  # ____________________________(PROFILE)_________________________
def deleteBlog(request, id):
  blog = Blog.objects.get(id=id)
  if blog.author == request.user:
    blog.delete()
  # return redirect(reverse('profile', args=[request.user.id]))
  return redirect(f'/profile/{request.user.id}')
