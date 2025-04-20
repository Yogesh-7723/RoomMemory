from django.shortcuts import render,redirect
from .models import Product,User,Album
from django.db.models import Sum
from datetime import datetime,date
from django.contrib.auth import get_user_model
from django.contrib.auth import  logout, authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
import random
from django.conf import settings

today = date.today()

def photo_picker():
    photos = Album.objects.all().values_list('photo',flat=True)
    return random.choice(photos)

# Create your views here.
def index(request):
    def media_path(file):
        return settings.MEDIA_URL + file
    data = User.objects.order_by("?")
    context = {
        'img1':media_path(photo_picker()),
    'img2' : media_path(photo_picker()),
    'img3' : media_path(photo_picker()),
    'img4' : media_path(photo_picker()),
    'data':data
    }
    return render(request,'index.html',context=context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.warning(request,"Password Not Match ")
            return redirect('/signup/')
        
        elif User.objects.filter(username=username).exists():
            messages.warning(request,"user already exists")
            return redirect('/signup/')
        else:
            pwd = make_password(password1)
            User.objects.create(username=username,email=email,password=pwd)
            messages.success(request,"Congrates Membership Successfull")
            return redirect('/sign_in/')
    else:
        return render(request,'accounts/signup.html')

def signin(request): 
    if request.method == 'POST':
        name = request.POST['username']
        pwd = request.POST.get('password')
        user = authenticate(username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"login Successfull")
            return redirect('/')
        else:
            messages.warning(request,"Invalid username and password")
            return redirect('/sign_in/')
    return  render(request,'accounts/signin.html')


def log_out(request,qk):
    user = User.objects.get(id=qk)
    if user is not None:
        logout(request)
    return redirect('/sign_in/')

class profile(APIView):
    def get(self,request,format=None):    
        user = request.user
        data = User.objects.get(username=user)
        product = Product.objects.filter(user=user)
        total = Product.objects.filter(user=request.user,created_at__day = today.day).aggregate(today = Sum('price'))
        current = Product.objects.filter(user=request.user,created_at__month=today.month).aggregate(month = Sum('price'))
        return render(request,"accounts/profile.html",{'data':data,'product':product,'current':current,'total':total})
    
    def post(self,request,format=None):
        data = User.objects.get(username=request.user)
        data.address = request.PATCH['address']
        data.state = request.PATCH['state']
        data.date_of_birth = request.PATCH['date_of_birth']
        data.gender = request.PATCH['gender']
        data.contact = request.PATCH['contact']
        data.profile = request.FILES.get('profile')
        data.save()
        product = Product.objects.filter(user=request.user)
        total = Product.objects.filter(user=request.user,created_at__day = today.day).aggregate(today = Sum('price'))
        current = Product.objects.filter(user=request.user,created_at__month=today.month).aggregate(month = Sum('price'))
        return render(request,"accounts/profile.html",{'data':data,'product':product,'current':current,'total':total})
    



def data(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            item = request.POST['item']
            price = request.POST['price']
            if user =='' or item == '' or price == '':
                messages.warning(request,"Enter Every Values")
            else:
                Product.objects.create(user=user,item=item,price=price)
                messages.success(request,"Item Successfully Add !")
                return redirect('/add_product/')
    
        u_data = User.objects.all()
        return render(request,'data.html',{'u_data':u_data})

def menu(request):
    return render(request,"menu.html")

def all_product(request):
    data = Product.objects.all()
    total = Product.objects.filter(user=request.user,created_at__day = today.day).aggregate(today = Sum('price'))
    current = Product.objects.filter(user=request.user,created_at__month=today.month).aggregate(month = Sum('price'))
    return render(request,'table.html',{'data':data,'total':total,'current':current})

def delete_data(request,qk):
    Product.objects.get(id=qk).delete()
    messages.success(request,"Product Successfully Delete.")
    return redirect('/profile/')


def all_profile(request,name):
    data = User.objects.get(username=name)
    data.title = "Jai ShiyaRam ji"
    return redirect("/profile/",{'data':data})

def album(request):
    if request.user.is_authenticated:    
        if request.method == 'POST':
            photo = request.POST['photo']
            caption = request.POST['caption']
            if photo:
                album = Album(user_name=request.user,photo=photo,caption=caption)
            else:
                messages.warning(request,"Photo Required !")
                return redirect('/album/')
    photos = Album.objects.all()
    return render(request,'album.html',{'images':photos})


def newalbum(request):
    return render(request,'newphoto.html')
