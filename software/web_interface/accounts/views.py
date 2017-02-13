from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.cache import cache_page
from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import get_token

from accounts.models import User, UserProfile
from accounts.forms import UserForm, UserProfileForm, TestPostForm

def home(request):
    return render(request, "accounts/home.html")

def profile(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        user = User.objects.get(username=username)
        #user_profile = UserProfile.objects.get(user=user)
        return render(request, "accounts/profile.html", {'user': user})
    else:
        return render(request, "accounts/profile.html")

def test_post(request):
    success = False

    if request.method == 'GET':
        return render(request, "personal/blank.html")
    elif request.method == 'POST':
        post_form = TestPostForm(data = request.POST)

        if post_form.is_valid():
            post = post_form.save()
            post.save()
            success = True
        else:
            print("errors", post_form.errors)
            print("non form errors", post_form.non_field_errors())
    else:
        post_form = TestPostForm()

    return render(request, 'accounts/testpost.html',
                  {
                      'post_form': post_form,
                      'success': success,
                  })

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
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Your account has been disabled.')

        else:
            print("Invalid login details.")
            return HttpResponse("Invalid login details supplied.")



    else:
        return HttpResponseRedirect('/')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
