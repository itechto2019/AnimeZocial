from django.shortcuts import redirect, render
from . models import Feed, Like,Topic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from . forms import FeedForm, UserForm,CommentForm
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import PasswordChangeForm

def indexPage(request):
    if request.user.is_authenticated :
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        feeds = Feed.objects.all()
        feeds = Feed.objects.filter(
            Q(body__icontains=q)|
            Q(topic__title__icontains=q)|
            Q(user__username__icontains=q)
        )
    else:
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        feeds = Feed.objects.all()[0:3]
        feeds = Feed.objects.filter(
            Q(body__icontains=q)|
            Q(topic__title__icontains=q)|
            Q(user__username__icontains=q)
        )[0:3]
    topics = Topic.objects.all()
    topics_count = Topic.objects.count()
    recents = Feed.objects.all().order_by('-updated', '-created')[0:8]

    context = {
        'feeds': feeds,
        'topics' : topics,
        'topics_count':topics_count,
        'recents' : recents
    }
    return render(request, 'pages/index.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try: 
            user = User.objects.get(username=username)             
        except:
            messages.error(request, "Username doesn't exist.")
            return redirect('login')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request, "Incorrect password")
            return redirect('login')
    return render(request, 'pages/login.html')

def registerPage(request):
    if request.user.is_authenticated :
        return redirect('index')
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('index')
        else:
            messages.error(request, "Please check your registration fields")
    context = {
        'form' : form
    }
    return render(request, 'pages/register.html', context)
def changePassword(request):
    form = PasswordChangeForm(user=request.user,data=request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            if form is not None:
                return redirect('profile-info', request.user.username)
            else:
                messages.error(request, "Incorrect old password")
                return redirect('change-password')
        else:
            messages.error(request, "Password mismatch")            
            return redirect('change-password')            
    context = {
        'form' : form
    }
    return render(request, 'profiles/change-password.html', context)

@login_required(login_url="/login")
def logoutUser(request):
    logout(request)
    return redirect('index')

@login_required(login_url="/login")
def createFeed(request):
    form = FeedForm()
    if request.method == "POST":
        form = FeedForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect('index')
    context = {
        'form' : form
    }
    return render(request, 'feeds/create-feed.html',context)

@login_required(login_url="/login")
def updateFeed(request, id):
    form = FeedForm()
    feed = Feed.objects.get(id=id, user=request.user)
    form = FeedForm(instance=feed)
    if request.method == "POST":
        form = FeedForm(request.POST,instance=feed)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {
        'form' : form
    }
    return render(request, 'feeds/edit-feed.html',context)

@login_required(login_url="/login")
def deleteFeed(request, id):
    feed = Feed.objects.get(id=id)
    if request.user != feed.user:
        return redirect('index')
    if request.method == "POST":
        feed.delete()
        return redirect('index')
    context = {
        'feed' : feed
    }
    return render(request, 'feeds/delete-feed.html',context)

@login_required(login_url="/login")
def profilePage(request, username) :
    user = User.objects.get(username=username)
    feeds = user.feed_set.all()
    recents = user.feed_set.all()
    topics = Topic.objects.all()
    form = UserForm()

    context ={
        'user' : user,
        'feeds': feeds,
        'recents' : recents,
        'topics' : topics,
        'form' : form,
    }
    return render(request,'profiles/profile-info.html',context)

@login_required(login_url="/login")
def profileUpdate(request) :
    user = User.objects.get(username=request.user)
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile-info', request.user.username)
    context ={
        'form' : form
    }
    return render(request,'profiles/profile-update.html',context)

@login_required(login_url="/login")
def likeFeed(request, id):
    feed = Feed.objects.get(id=id)
    user = request.user
    if request.method == "POST":
        check = Like.objects.filter(user=user, feed=feed)
        if check.exists():
            check.delete()
        else:
            Like.objects.create(
                state = True,
                user = user,
                feed = feed
            )
            feed.likes.add(user)
    return redirect('index')

@login_required(login_url="/login")
def feed(request, user, topic, id):
    form = CommentForm()
    feed = Feed.objects.get(id=id)
    comments = feed.comment_set.all().order_by('-updated')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)        
            comment.user = request.user
            comment.feed = feed
            comment.body = request.POST.get('body')
            comment.save()
            feed.comments.add(comment)
            return redirect('feed', user=user,topic=topic, id=id)
    context = {
        'feed': feed,
        'comments':comments,
        'form': form
    }
    return render(request, 'feeds/comment-feed.html', context)