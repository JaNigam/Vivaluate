
import imp
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import pytesseract
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from .forms import CreateUserForm
import random,string
from .decorators import *



@authenticated_user
def logoutUser(request):
    logout(request)
    return redirect("/login")


@csrf_exempt
@unauthenticated_user
def Login(request):
    context={}
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
           messages.info(request,"Username or password incorrect")             
     
    return render(request,'login.html',context)


@authenticated_user
def addStudent(request):
    if(request.method=="POST"):
        try:
            code=request.POST["code"]
            classroom=Classroom.objects.get(code=code)
            student=Student.objects.get(user=request.user)
            classroom.student.add(student)
            classroom.save()
        except:
             messages.info(request,"Doesnt exist")  
        
        return redirect("/")
    return render(request,"classlist.html")

def Test(request):
    if request.user.groups.filter(name='Student').exists():
         classroom=Classroom.objects.filter(student=Student.objects.get(user=request.user))
         return render(request,"Test.html",{"classroom":classroom})
    if request.user.groups.filter(name='Teacher').exists():
         classroom=Classroom.objects.filter(teacher=Teacher.objects.get(user=request.user))
         return render(request,"Test.html",{"classroom":classroom})

    return render(request,"Test.html")
    

def index(request):
    s=""
    if (request.method=="POST"):
        img=request.FILES["answersheet"]
        img=Image.open(img)
        s=(pytesseract.image_to_string(img))
        

    return render(request,"index.html",{"s":s})

@unauthenticated_user
@csrf_exempt
def registerPage(request):
    form=CreateUserForm()
    
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            group=Group.objects.get(name='Student')
            user.groups.add(group)
            name=request.POST["Name"]
            login(request,user)
            s=Student.objects.create(user=user,name=name)
            s.save()
            messages.success(request,"Account was created")
            return redirect("/")
    context={'form':form}
    return render(request,'register.html',context)\



@csrf_exempt
@unauthenticated_user
def registerPageTeacher(request):
    form=CreateUserForm()
    
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            group=Group.objects.get(name='Teacher')
            user.groups.add(group)
            name=request.POST["Name"]
            login(request,user)
            s=Teacher.objects.create(user=user,name=name)
            s.save()
            messages.success(request,"Account was created")
            return redirect("/")
    context={'form':form}
    return render(request,'register.html',context)


def addClassroom(request):
    s=''.join(random.choices(string.ascii_uppercase+string.ascii_lowercase+ string.digits, k=6))
    if request.method=="POST":
        name=request.POST["classname"]
        s=Classroom.objects.create(teacher=Teacher.objects.get(user=request.user),code=s,name=name)
        s.save()
        return redirect("/teacher")
    return render(request,'addclass.html',{"s":s})


@allowed_users(["Student"])
def classlist(request):
    s=Classroom.objects.filter(student=Student.objects.get(user=request.user))
    return render(request,'classlist.html',{"s":s})


@allowed_users(["Teacher"])
def TeacherLandingPage(request):
    s=Classroom.objects.filter(teacher=Teacher.objects.get(user=request.user))
    return render(request,'teacher_landing_page.html',{"s":s})


def MainIndex(request):
    if request.user.groups.filter(name='Student').exists():
         return redirect("/student")
    if request.user.groups.filter(name='Teacher').exists():
         return redirect("/teacher")
    if not request.user.is_authenticated:
        return redirect("/login")
    return redirect("/login")


def studentList(request,pk):
    s=Classroom.objects.get(id=pk)
    t=s.student.all()
    return render(request,"studentList.html",{"t":t})