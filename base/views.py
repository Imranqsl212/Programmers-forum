from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from django.db.models import Q
from .forms import RoomForm, userForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


# rooms = [
#     {
#         'id': 1,
#         'name': 'Back-end devops'
#     },
#     {
#         'id': 2,
#         'name': 'Designers'
#     }
#     {
#         'id': 3,
#         'name': 'Front-end Devops'
#     }
# ]


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(desc__icontains=q)
    )

    topics = Topic.objects.all()[0:3]
    room_count = rooms.count()
    messages1 = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'messages1': messages1}
    return render(request, 'base/home.html', context)


@login_required(login_url='Log_in')
def room(request, pk):
    room = Room.objects.get(id=pk)
    messages1 = room.message_set.all()
    members = room.participants.all()
    context = {'room': room, 'messages1': messages1, 'members': members}
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('send')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    return render(request, 'base/room.html', context)


@login_required(login_url='Log_in')
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    messages1 = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'messages1': messages1, 'topics': topics}
    return render(request, 'base/userProfile.html', context)


@login_required(login_url='Log_in')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            desc=request.POST.get('desc'),

        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_forum.html', context)


@login_required(login_url='Log_in')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You arent owner of a room')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.desc = request.POST.get('desc')
        room.topic = topic
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_forum.html', context)


@login_required(login_url='Log_in')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You arent owner of a room')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='Log_in')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You arent owner of a message')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('pass')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User doesnt exists')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User OR password doesnt exists')
    context = {'page': page}
    return render(request, 'base/log_reg.html', context)


@login_required(login_url='Log_in')
def updateUser(request):
    user = request.user
    form = userForm(instance=user)
    context = {'form': form}
    if request.method == 'POST':
        form = userForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)
    return render(request, 'base/edit-user.html', context)


def registerPage(request):
    form = UserCreationForm()
    context = {'form': form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/log_reg.html', context)


def activities(request):
    messages1 = Message.objects.all()
    context = {'messages1': messages1}

    return render(request, 'base/activities.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)
