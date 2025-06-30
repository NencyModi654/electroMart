from django.urls import path
from . import views

urlpatterns=[
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerSeller/',views.registerSeller,name='registerseller'),
    path('login/',views.login,name='login'),
    path('myAccount/',views.myAccount,name='myAccount'),
    path('logout/',views.logout,name='logout'),
    path('custDashboard/',views.custdashboard,name='custdashboard'),
    path('sellerDashboard/',views.sellerdashboard,name='sellerdashboard'),

]