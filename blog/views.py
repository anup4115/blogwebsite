from django.shortcuts import render, redirect,HttpResponse
from . models import Post, Contact
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages #import message
# Create your views here.

def blog(request):
    post=Post.objects.all() #data taneko Post model ko
    return render(request,'blog.html',{'post':post}) #to  print data in frontend 

def contact(request):
    if request.method=="POST":
        name=request.POST['name']                                                                   #request.POST.get('name') le empty pani accept garxa
        phone=request.POST['phone']
        email=request.POST['email']
        content=request.POST['content']
        obj_cont=Contact(name=name,phone=phone,email=email,content=content)                          #LHS model ko ra RHS ko yeskai
        obj_cont.save()
    return render(request,'contact.html')

def home(request):
    data=Post.objects.all()
    return render(request,'home.html',{'data':data})

def SignUp(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        username=request.POST['uname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if pass1==pass2:
            user=User.objects.create_user(username=username,password=pass1)
            return redirect('home')
        
def Handlelogin(request):
    if request.method=="POST":
        username=request.POST['loginusername']
        pass1=request.POST['loginpassword']
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            messages.success(request,'You are successfully login')
            return redirect('contact')
        else:
            messages.error(request,"User does not exists")
            return redirect('home')
    else:
        return HttpResponse("user does not exist")
    
def Search(request):
    query=request.GET['query']
    data1=Post.objects.filter(title__icontains=query)
    data2=Post.objects.filter(author__icontains=query)
    data3=Post.objects.filter(slug__icontains=query)
    data=data1.union(data2,data3)
    return render(request,'search.html',{'data':data})

def blogPost(request, slug):
    post=Post.objects.filter(slug=slug).first() #get
    return render(request,'blogpost.html',{'post':post})
    
        