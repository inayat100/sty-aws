from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    path('contact/',views.contact,name='contact'),
    path('singin/',views.singin,name='singin'),
    path('logout/',views.user_logout,name='logout'),
    path('singup/',views.singup,name='singup'),
    path('basebord/',views.dasebord,name='dasebord'),
    path('full_post/<int:id>/',views.full_post,name='full_post'),
    path('update/<int:id>/',views.update,name='update'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('like/',views.like,name='like'),
    path('comment',views.comment,name='comment'),
    path('reply',views.reply,name='reply'),
    path('search/',views.search,name='search'),
]