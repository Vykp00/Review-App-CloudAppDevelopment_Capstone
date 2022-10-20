from multiprocessing import context
from unittest import result
from urllib import request
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from djangoapp.models import Profile
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from djangoapp.forms import EditProfileForm, SignupForm
from django.contrib.auth.decorators import login_required

from djangoapp.restapis import get_dealer_by_id, get_dealers_from_cf,get_dealers_by_state,get_dealer_reviews_from_cf,post_request
from djangoapp.models import CarModel, CarDealer, CarMake, DealerReview

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# Index view
def index(request):
    user = request.user
    context = {}
    return render(request, 'djangoapp/index.html', context)


# Create an `about` view to render a static about page
def about (request):
    user=request.user
    context={}
    return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    user= request.user
    context={}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context={}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Edit profile views
@login_required
def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile.location = form.cleaned_data.get('location')
            profile.email = form.cleaned_data.get('email')
            profile.url = form.cleaned_data.get('url')
            profile.profile_info = form.cleaned_data.get('profile_info')
            profile.save()
            return redirect('djangoapp:index')
    else:
        form = EditProfileForm(instance=profile)

    context = {
        'form': form,
    }
    return render(request, 'djangoapp/edit_profile.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def Registration(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password')
            user=User.objects.create_user(
                username=username, password=password, first_name=first_name, last_name=last_name
            )
            login(request, user)
            return redirect('djangoapp:edit-profile')
    else:
        form = SignupForm()
    
    context={
        'form': form,
    }
    return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
#def get_dealerships(request):
 #   context = {}
  #  if request.method == "GET":
   #     return render(request, 'djangoapp/index.html', context)
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = 'https://eu-de.functions.appdomain.cloud/api/v1/web/vy.le9824%40gmail.com_mydev-de/dealership-package/get-dealership.json'
        # Get dealers from the URL
        context["dealerships"] = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)
            

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = 'https://eu-de.functions.appdomain.cloud/api/v1/web/vy.le9824%40gmail.com_mydev-de/dealership-package/get_review'
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context = {
            "reviews": reviews,
            "dealer_id": dealer_id,
        }

        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    # Verify the user is authenticated
    if request.user.is_authenticated:
        # GET request renders the page with the form for filling out a review
        if request.method == "GET":
            url = "https://5b93346d.us-south.apigw.appdomain.cloud/dealerships/dealer-get?dealerId={dealer_id}"
            # Get dealer details from the API
            context = {
                "cars": CarModel.objects.all(),
                "dealer": get_dealer_by_id(url, dealer_id=dealer_id),
            }
            return render(request, 'djangoapp/add_review.html', context)
        # POST request posts the content in the review submission form to the Cloudant DB using the post_review Cloud Function
        if request.method == "POST":
            form = request.POST
            review = dict()
            review["name"] = "{request.user.first_name} {request.user.last_name}"
            review["dealership"] = dealer_id
            review["review"] = form["content"]
            review["purchase"] = form.get("purchasecheck")
            if review["purchase"]:
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%d/%m/%Y").isoformat()
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.year

            # If the user bought the car, get the purchase date
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%d/%m/%Y").isoformat()
            else:
                review["purchase_date"] = None

            url = "https://eu-de.functions.appdomain.cloud/api/v1/web/vy.le9824%40gmail.com_mydev-de/dealership-package/post-review"
            json_payload = {"review": review}
            result = post_request(url, json_payload, dealerId=dealer_id)
            if int(result.status_code) == 200:
                print("Review posted successfully.")

            # After posting the review the user is redirected back to the dealer details page
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

        else:
            # If user isn't logged in, redirect to login page
            print("Please login in to post a review")
            return redirect("/djangoapp/login")


