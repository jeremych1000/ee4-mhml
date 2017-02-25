from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from sendfile import sendfile

from myaccount.forms import UserForm, UserProfileForm, TestPostForm
from myaccount.models import User
from web_interface.decorators import login_required, login_required_message_and_redirect

@login_required_message_and_redirect(message="You need to be signed in to view this page.")
def profile(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        user = User.objects.get(username=username)
        # user_profile = UserProfile.objects.get(user=user)
        return render(request, "myaccount/profile.html", {'user': user})
    else:
        return render(request, "myaccount/profile.html")

@login_required_message_and_redirect(message="You need to be signed in to view this page.")
def preferences(request):
    # !!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!
    # should be getting preferences model, not user model
    # !!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        user = User.objects.get(username=username)
        # user_profile = UserProfile.objects.get(user=user)
        return render(request, "myaccount/preferences.html", {'user': user})
    else:
        return render(request, "myaccount/preferences.html")

@login_required_message_and_redirect(message="You need to be signed in to view this page.")
def stats(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
        return render(request, "myaccount/statistics.html")
    else:
        return render(request, "myaccount/statistics.html")

def test_post(request):
    success = False

    if request.method == 'GET':
        return render(request, "personal/blank.html")
    elif request.method == 'POST':
        post_form = TestPostForm(data=request.POST)

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
    # create boolean to see if successfully registered
    registered = False

    if request.method == 'POST':
        # get information from post request
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # save form to database
            user = user_form.save()
            user.set_password(user.password)

            user.save()

            profile = profile_form.save(commit=False)  # delay saving to database until verified
            profile.user = user  # populate the user model instance for the one to one mapping

            # see if provided profile pictures etc
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:  # not a POST request
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'myaccount/register.html',
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


@login_required
def dl(request):
    return sendfile(request,
                    'C:/Users/Jeremy/Documents/GitHub/ee4-mhml/software/web_interface/media/data/MSBand2_ALL_data_15_02_17.csv',
                    attachment=True, attachment_filename='test.csv')
