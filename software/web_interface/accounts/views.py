from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from accounts.forms import UserForm, UserProfileForm


# Create your views here.
#@login_required(login_url="accounts/login/")

def home(request):
    return render(request, "accounts/home.html")

def register(request):
    #create boolean to see if successfully registered
    registered = False

    if request.method == 'POST':
        #get information from post request
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #save form to database
            user = user_form.save()
            user.set_password(user.password)

            user.save()

            profile = profile_form.save(commit=False) #delay saving to database until verified
            profile.user = user #populate the user model instance for the one to one mapping

            #see if provided profile pictures etc
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else: # not a POST request
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'accounts/register.html',
                  {
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered,
                  })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Your account has been disabled.')
        else:
            print("Invalid login details.")
            return HttpResponse("Invalid login details supplied.")

        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

    else:
        return HttpResponseRedirect('/')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
