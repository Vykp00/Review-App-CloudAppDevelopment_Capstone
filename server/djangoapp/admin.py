from django.contrib import admin
from .models import Profile, CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.TabularInline):
    model= CarModel
    extra= 2
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display=('name','dealer_id','cartype')
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines=[CarModelInline]
    list_display=['name']

# Register models here
admin.site.register(Profile)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)