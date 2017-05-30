from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from main.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime

##from i2c.i2c_lib import i2c_get_status
##from i2c.i2c_lib import i2c_get_config

from lighting.models import LightingState
from i2c.models import Device


def get_server_side_cookie(request, cookie, default_val=None):
        val = request.session.get(cookie)
        if not val:
                val = default_val
        return val


def visitor_cookie_handler( request ):
        # Get the number of visits to the site.
        # We use the COOKIES.get() function to obtain theh visits cookie.
        # If the cookie exists, the value returned is cast to an integer.
        # If the cookie doesn't exist, then the default value of 1 is used.
        visits = int(get_server_side_cookie(request, 'visits', '1'))
        last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
        last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

        # If it's been more than a day since the last visit...
        if (datetime.now() - last_visit_time).days > 0:
                visits = visits + 1
                # Update the lst viist cookie now that we have updated the count
                request.session['last_visit'] = str(datetime.now())
        else:
                visists = 1
                # Set the last visit cookie
                request.session['last_visit'] = last_visit_cookie

        # Update/Set the visit cookie
        request.session['visits'] = visits





def index( request ):
        request.session.set_test_cookie()
        context_dict = {'pagetitle': 'Our House',
                        'pagename' : 'Our Hourse - Start'}

        # Call the function to handle the cookies
        visitor_cookie_handler(request)
        context_dict['visits'] = request.session['visits']
        response = render(request, 'index.htm', context=context_dict)

        return response

def dashboard( request , status_dict=None):
        if status_dict == None:
                print("Calling the dashboard refresh for the first time")
                return dashboard_refresh( request )
        print("STATUS_DICT=" + str(status_dict))
        response = render(request, 'main/dashboard.htm', context=status_dict)
        return response

def dashboard_refresh( request ):
##        status_int = i2c_get_status( 32 )
##        config_int = i2c_get_config( 32 )
        device = Device.objects.get(name="Lighting")
        history = LightingState.objects.get(device = device)
        status_int = history.status
        config_int = history.config
        print("status {0:08b}, config {1:08b}".format(status_int, config_int))
        status_dict = {"UG_State": "DISABLED", "EG_State": "DISABLED", "OG_State": "DISABLED" }
        
        if config_int & 0b00010000 >= 1:
                print("Setting UG to OFF")
                status_dict["UG_State"]="OFF"
        if config_int & 0b00100000 >= 1:
                print("Setting EG to OFF")
                status_dict["EG_State"]="OFF"
        if config_int & 0b01000000 >= 1:
                print("Setting OG to OFF")
                status_dict["OG_State"]="OFF"
           
        if status_int & 0b00000001 >= 1:
                print("Setting UG to ON")
                status_dict["UG_State"] = "ON"
        if status_int & 0b00000010 >= 1:
                print("Setting EG to ON")
                status_dict["EG_State"] = "ON"
        if status_int & 0b00000100 >= 1:
                print("Setting OG to ON")
                status_dict["OG_State"] = "ON"

        print("status_refresh status_dict=" + str(status_dict))
                
        return dashboard( request, status_dict=status_dict )


def about( request ):
        if request.session.test_cookie_worked():
                print("THE TEST COOKIE WORKED")
                request.session.delete_test_cookie()
        context_dict = {'pagetitle': 'Our House',
                        'pagename' : 'Our Hourse - About'}
        return render(request, 'about.htm', context=context_dict)


##def register( request ):
##        # A boolean value for telling the template
##        # whether the registration was successful.
##        # Set to False initially. Code changes value to
##        # True when registration succeeds.
##        registered = False
##
##        # If it's a HTTP POST, we're interested in processing from data
##        if request.method == 'POST':
##                # Attempt to grab information from the raw form information.
##                # Note that we make use of both UserForm and UserProfileForm.
##                user_form = UserForm(data=request.POST)
##                profile_form = UserProfileForm(data=request.POST)
##
##                # If the two forms are valid...
##                if user_form.is_valid() and profile_form.is_valid():
##                        # Save the user's form data to the database.
##                        user = user_form.save()
##
##                        # Now we hash the password with the set_password method
##                        # Once hashed, we can u pdate the user object
##                        user.set_password(user.password)
##                        user.save()
##
##                        # Now sort out the UserProfile instance.
##                        # Since we need to set the user attribute ourselves
##                        # we set commit=False. This delays saving the model
##                        # until we're ready to avoid integrity problems.
##                        profile = profile_form.save(commit=False)
##                        profile.user = user
##
##                        # Did teh user provide a profile picture?
##                        # If so, we need to get it from the input Form and
##                        # put it in the UserProfile model.
##                        if 'picture' in request.FILES:
##                                profile.picture = request.FILES['picture']
##
##                        # Now we save the UserProfile model instance.
##                        profile.save()
##
##                        # Update our variable to indicate that the tempalte
##                        # registration was successful
##                        registered = True
##
##                else:
##                        # Invalid form or forms - mistakes or something else?
##                        # Print the problem to the terminal
##                        print(user_form.errors, profile_form.errors)
##        else:
##                # Not a HTTP POST, so we render out form using two ModelForm instances.
##                # These forms will be blank, ready for user input.
##                user_form = UserForm()
##                profile_form = UserProfileForm()
##
##        # Render the template depending on the context.
##        return render(request, 'register.htm',
##                      {'user_form': user_form,
##                       'profile_form': profile_form,
##                       'registered': registered})
##
##
##def user_login( request ):
##        # If the requst is a HTTP POST, try to pull out the relevant information
##        if request.method == 'POST':
##                # Gather the username and passwrod provided by the user.
##                # This information is obtained from the login form.
##                # We use request.POST.get('<variable>') as opposed
##                # to requst.POST['<variable>'], because the
##                # request.POST.get('<variable>') returns None if the
##                # value does not exist, while request.POST['<variable>']
##                # will raise a KeyError exception.
##                username = request.POST.get('username')
##                password = request.POST.get('password')
##
##                # Use Django's machinery to attempt to see if the username/password
##                # combination is valid - a User object is returned if it is.
##
##                user = authenticate(username=username, password=password)
##
##                # If we have a User object, the details are correct.
##                # If None (Python's way of representing the absense of a value), no user
##                # with matchin credentials was found.
##                if user:
##                        # Is the account active? It could have been disabled
##                        if user.is_active:
##                                # If teh account is valid and active, we can log the use in.
##                                # We'll send the user back to the homepage.
##                                login(request, user)
##                                return HttpResponseRedirect(reverse('index'))
##                        else:
##                                # An inactive acctoun was used - no logging in
##                                return HttpResponse("Your Our House account is disabled")
##                else:
##                        # Bad login details were provided. So we can't log the user in
##                        print("Invalid login details: {0}, {1}".format(username, password))
##                        # return HttpResponse("Invalid login details")
##                        return render( request, 'login.htm', {'form_error': 'Invalid login details'})
##        # The request is not a HTTP POST, so display the login form.
##        # This scenario would most likely be a HTTP GET.
##        else:
##                # No context variables to pass to the template system, hence the
##                # blank dictionary object
##                return render( request, 'login.htm', {'form_error': ''})
##        
##                
##@login_required
##def user_logout( request ):
##        # Since we know the user is logged in, we cna now just log them out
##        logout( request )
##        # Take the user back to the home page
##        return HttpResponseRedirect(reverse('main:index'))
##
