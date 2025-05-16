from django.shortcuts import render
from UserApp.forms import NewUserForm,UserProfileForm
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'UserApp/index.html',{})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = NewUserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            registered = True
            profile.save()

        else:
            return HttpResponse(user_form.errors,profile_form.errors)
    
    else:
        user_form = NewUserForm()
        profile_form = UserProfileForm()

    return render(request,'UserApp/register.html',{
        'user_form':user_form,
        'profile_form':profile_form,
        'registered':registered
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponse('Logged In Successfully !')
            else:
                return HttpResponse('Account Inactive !')
        else:
            return HttpResponse('Invalid Login Credentials !')
    else:
        return render(request,'UserApp/login.html',{})
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('UserApp:index'))