from unicodedata import name
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth import views as authViews 
from djangoapp.views import login_request, EditProfile, Registration, logout_request

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path('', views.index, name='home'),
    path('', views.get_dealerships, name='index'),
    # path for about view
    path('djangoapp/about', views.about, name='about'),

    # path for contact us view
    path('djangoapp/contact', views.contact, name='contact'),
    # path for edit profile
    path('profile/edit', EditProfile, name='edit-profile'),

    # path for registration
    path('registration/', Registration, name='registration'),

    # path for login
    path('login/', views.login_request, name='login'),
    # path for logout
    path('logout/', views.logout_request, name='logout'),

    #path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path(route='dealer/<int:dealer_id>/add-review/', view=views.add_review, name="add_review"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)