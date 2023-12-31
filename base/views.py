from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Room, Topic, Messages, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.contrib.auth.decorators import login_required

# rooms = [
#     {"id":1, "name":"Let's learn Python"},
#     {"id":2, "name":"Let's learn Design"},
#     {"id":3, "name":"Let's learn Django"}
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        # print(username)
        # print(username)
        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, "User don't exists")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            print(user)
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "User don't exists")
            
    context = {'page' : page}
    return render(request, 'base/login_reg.html', context)

def logoutUser(request):
    logout(request)
    return redirect("home")

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured!')

    return render(request, 'base/login_reg.html', {'form' : form})

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
        )
    # rooms = Room.objects.all()
    topics = Topic.objects.all()[0:3]
    room_count = rooms.count()
    room_msgs = Messages.objects.filter(Q(room__topic__name__icontains =q))

    context = {"rooms" : rooms, "topics" : topics, "room_count" : room_count, 'room_msgs' : room_msgs}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_msgs = room.messages_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        msg = Messages.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    return render(request, 'base/room.html',{
        "room" : room,
        "msgs" : room_msgs,
        'participants' : participants
    })

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_msg = user.messages_set.all()
    topics = Topic.objects.all()
    context = {'user' : user, 'rooms' : rooms, 'room_msgs' : room_msg, 'topics' : topics}
    return render(request, 'base/profile.html',context)

@login_required(login_url='/login')
def create_room(request):
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        
    
    return render(request, 'base/room_form.html', {
        "form" : RoomForm(),
        "topics" : topics
    })

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name =request.POST.get('name')
        room.topic = topic
        room.description =request.POST.get('description')
        room.save()
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect("home")
    
    return render(request, 'base/room_form.html', {
        'form' : form,
        'topics' : topics,
        'room' : room
    })

@login_required(login_url='/login')
def del_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {
        'obj' : room
    })

@login_required(login_url='/login')
def del_msg(request, pk):
    msg = Messages.objects.get(id=pk)
    if request.user != msg.user:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        msg.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {
        'obj' : msg
    })

@login_required(login_url='login')
def updateUser(request):    
    user = request.user
    form = UserForm(instance=request.user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {
      'form' : form
    })

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "base/topics.html", {
        'topics' : topics
    })

def activityPage(request):
    room_msgs = Messages.objects.all()
    return render(request, "base/activity.html", {
        'room_msgs' : room_msgs
    })