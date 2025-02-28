from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse

from django.contrib.auth.decorators import login_required

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')



def registration(request):
        UFD=UserForm()
        PFD=ProfileForm()
        d={'UFD':UFD,'PFD':PFD}
        if request.method=='POST' and request.FILES:
              UFD=UserForm(request.POST)
              PFD=ProfileForm(request.POST,request.FILES)
              if UFD.is_valid() and PFD.is_valid():
                NSUO=UFD.save(commit=False)
                password=UFD.cleaned_data['password']
                NSUO.set_password(password)
                NSUO.save()
                NSPO=PFD.save(commit=False)
                NSPO.username=NSUO
                NSPO.save()
                send_mail('Registratioon',
                        "Succefully Registration",
                      'vgowthami1930@gmail.com',
                      [NSUO.email],
                      fail_silently=False
                      )
                return HttpResponse('Registration Success')
              else:
                  return HttpResponse("NOT VALID")
        return render(request,'login.html',d)
def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)

        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('u r not an authenticated user')
    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def eight(request):
    return render(request,'eight.html')



def payment(request):
    return render(request,'payment.html')



def reset_password(request):

    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST.get('pw')

        LUO=User.objects.filter(username=un)

        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('password reset is done')
        else:
            return HttpResponse('Reset password is done successfully')
    return render(request,'reset_password.html')



@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['password']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('Password is changed successfully')
    return render(request,'change_password.html')


def reset_password(request):
    if request.method=="POST":
        un=request.POST['un']
        pw=request.POST['pw']
        LUO=User.objects.filter(username=un)
        if LUO:
            LUO[0].set_password(pw)
            LUO[0].save()
        else:
            return HttpResponse('Not Done')
    return render(request,'reset_password.html')