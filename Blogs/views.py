from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *

# Create your views here.
def home(request):
  blogs = Blog.objects.all()
  context = {'blogs':blogs}
  return render(request, "home.html", context)

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
  
    Blog.objects.create(
      title = title,
      content = content,
      author = request.user
    )
    messages.info(request, "Blog Created Success fully")
    print("Blog Created ")
    return redirect("/createBlog")
  return render(request, "createBlog.html")

def displayBlog(request):
  blogs = Blog.objects.all()
  context = {'blogs':blogs}
  return render(request, "displayblog.html", context)

def testingRequirement(request):
  user = User.objects.all()
  context = {'user':user}
  return render(request, "testingPage.html", context)

