from django.contrib import admin
from .models import POST,user_contact,user_comment,user_reply
# Register your models here.
# admin.site.register(test2)
@admin.register(POST)
class POST(admin.ModelAdmin):
    list_display = ['id','img','user','title','post']
    readonly_fields = ('date',)

@admin.register(user_contact)
class user_contact(admin.ModelAdmin):
    list_display = ['id','your_name','your_email','your_Number','write','date']
    readonly_fields = ('date',)

@admin.register(user_comment)
class comment(admin.ModelAdmin):
    list_display = ['id','user','post','comment']
    readonly_fields = ('date',)

@admin.register(user_reply)
class reply(admin.ModelAdmin):
    list_display = ['id','user','post','comment','reply']
    readonly_fields = ('date',)
