from django.contrib import admin
from .models import *
# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','phone','subject','message','created','status','closed','remark']
    list_display_links = ('id','name','phone')



class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','first_name','last_name','phone','address','state','image']
    list_display_links = ('user','first_name','last_name')



admin.site.register(Contact,ContactAdmin)
admin.site.register(Profile,ProfileAdmin)
