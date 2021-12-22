from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('login/',views.login,name="login"),
    path('login1/',views.login1,name="login"),
    path('signup/',views.signup.as_view(),name="signup"),
    path('logout/',views.logout),
    path('forgotpassword/',views.forgot),
    path('otp/',views.otp),
    path('checkotp/',views.checkotp),
    path('changepassword/',views.change),
    path('postpg/',views.postpg),
    path('postpg1/',views.postpg1.as_view()),
    path('getpg/',views.getpg1),
    path("sendmsg/",views.sendmsg),
    path("checkeotp/",views.checkeotp),
    path('getpg1/',views.getpg),
    path('getpg2/',views.getpg2),
    path('getpg3/',views.getpg3),
    path('getpg4/',views.getpg4),
    path('getpg5/',views.getpg5),
    path('getpg6/',views.getpg6),
]
