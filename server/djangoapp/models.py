import email
from email.policy import default
from multiprocessing.util import ForkAwareThreadLock
from random import choices
from statistics import mode
from tabnanny import verbose
from unicodedata import name
from unittest.mock import sentinel
from unittest.util import _MAX_LENGTH
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import sys
from django.db.models.signals import post_save
from django.conf import settings
import os
import uuid
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()



# Create your models here.
# Create Profile model to sign in
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    url = models.CharField(max_length=80, null=True, blank=True)
    profile_info = models.TextField(max_length=150, null=True, blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile.objects.get(user=user)
        profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_profile, sender=User)

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100, null=False, default='car make', verbose_name='Title')
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make= models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, default='car model', verbose_name='Title')
    dealer_id = models.IntegerField()
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
    ]
    cartype = models.CharField(null=False, max_length=10, choices=TYPE_CHOICES, default=SEDAN)
    year = models.DateField(null=True)

    def __str__(self):
        return self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer full name:
        self.full_name = full_name
        # Dealer id:
        self.id = id
        # Location latitude
        self.lat = lat
        # Location longitude
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zipcode
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, id, review, sentiment, **kwargs):
        
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.id = id
        self.review = review
        self.sentiment = sentiment
        
        if purchase:
            self.purchase_date = kwargs["purchase_date"]
            self.car_make = kwargs["car_make"]
            self.car_model = kwargs["car_model"]
            self.car_year = kwargs["car_year"]
        
        
    def __str__(self):
        return "Review: " + self.review