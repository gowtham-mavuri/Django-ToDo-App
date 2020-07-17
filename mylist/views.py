from django.contrib.auth import authenticate, logout,login as dj_login
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from mylist.models import todo
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        todo_items = todo.objects.filter(user=request.user).order_by("-added_date")
        return render(request,'mylist/index.html',{"todo_items":todo_items})
    else:
        return redirect("login")


@csrf_exempt
def add(request):
    date = timezone.now()
    content = request.POST["content"]
    cur_user = request.user
    obj = todo.objects.create(added_date=date,text=content,user=cur_user)
    messages.success(request, f"Added")
    return HttpResponseRedirect("/")

@csrf_exempt
def delete(request,todo_id):
    todo.objects.get(id=todo_id).delete()
    return HttpResponseRedirect("/")

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, f"Logged in Successully")
            print(user)
            dj_login(request,user)
            return HttpResponseRedirect("/")
        else:
            messages.success(request, f"Failed")
            return render(request, 'registration/login.html',{"username":username})
    else:
        username = ""
        return render(request, 'registration/login.html', {"username": username})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")

@csrf_exempt
def register(request):
    if request.method == 'POST':
        un = request.POST['username']
        ps = request.POST['password']
        em = request.POST['email']
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        l = len(User.objects.filter(username=un)) + len(User.objects.filter(email=em))
        if l == 0:
            User.objects.create_user(un,em,ps)
            user = authenticate(request, username=un, password=ps)
            user.last_name=ln
            user.first_name=fn
            user.save()
            messages.success(request, f"welcome Logged in Successully")
            dj_login(request,user)
            return HttpResponseRedirect("/")
        else:
            messages.success(request, f"already exists")
            return render(request, 'registration/registration.html',{"un":un,"ps":ps,"em":em,"fn":fn,"ln":ln})
    else:
        u = ""
        return render(request, 'registration/registration.html', {"un":u,"ps":u,"em":u,"fn":u,"ln":u})


def profile(request):
    user=request.user
    print(user.first_name)
    print(user)
    return render(request,'registration/profile.html',{"un":user.username,"ps":user.password,"em":user.email,"fn":user.first_name,"ln":user.last_name})