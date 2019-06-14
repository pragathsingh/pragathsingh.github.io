"""FoodExpress URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from django.contrib import admin
from django.urls import path
from .mycontroller import *

urlpatterns = [

    #main urls
    path('admin/', admin.site.urls),
    path('', indexpage, name='index'),

    #cuisine urls
    path('viewcuisines',viewcuisines,name='viewcuisines'),
    path('insertcuisinepage',insertcuisinepage,name='insertcuisinepage'),
    path('insertcuisineaction',insertcuisine,name='insertcuisineaction'),
    path('deletecuisine',deletecuisine,name='deletecuisine'),
    path('updatecusinepage',updatecuisinepage,name='updatecusinepage'),
    path('updatecuisineaction',updatecuisineaction,name='updatecusineaction'),

    #admin urls
    path('adminview',adminview,name='adminview'),
    path('adminaddpage',adminaddpage,name='adminaddpage'),
    path('addaction',adminaddaction,name='addadminaction'),
    path('adminsigninpage',adminsigninpage,name='adminsigninpage'),
    path('adminsigninaction',adminsigninaction,name='adminsigninaction'),
    path('adminupdateaction',adminupdateaction,name='adminupdateaction'),
    path('adminlogoutaction',adminlogoutaction,name='adminlogoutaction'),
    path('adminforgetpasswordpage', adminforgetpasswordpage, name='adminforgetpasswordpage'),
    path('adminupdateaction', adminupdateaction, name='adminupdateaction'),
    path('adminforgetpasswordaction', adminforgetpasswordaction, name='adminforgetpasswordaction'),
    path('adminforgetpasswordredirect/<random_link>', adminforgetpasswordredirect, name='adminforgetpasswordredirect'),
    path('adminchangepassword', adminchangepassword, name='adminchangepassword'),
    path('admindelete',admindelete,name='admindelete'),
    path('adminupdate',adminupdatepage,name='adminupdatepage'),
    path('adminapproverestaurant',adminapproverestaurant,name='adminapproverestaurant'),
    path('adminapproverestaurantpage',adminapproverestaurantpage,name='adminapproverestaurantpage'),
    path('adminrevokerestaurantapproval',adminrevokerestaurantapproval,name='adminrevokerestaurantapproval'),
    path('adminsettingspage',adminsettingspage,name='adminsettingspage'),
    path('adminsettingsaction',adminsettingsaction,name='adminsettingsaction'),
    #restaurent urls
    path('addrestaurentpage',addrestaurentpage,name='addrestaurantpage'),
    path('addrestaurantaction',addrestaurentaction,name='addrestaurantaction'),
    path('viewrestaurant',viewrestaurentpage,name='viewrestaurant'),
    path('deleterestaurant',deleterestaurentaction,name='deleterestaurant'),
    path('updaterestaurantpage',updaterestaurentpage,name='updaterestaurantpage'),
    path('updaterestaurantaction',updaterestaurentaction,name='updaterestaurantaction'),
    path('searchrestaurant',searchrestaurant,name='searchrestaurant'),
    path('restaurantsignuppage',restaurantsignuppage,name='restaurantsignuppage'),
    path('restaurantsignupaction',restaurantsignupaction,name='restaurantsignupaction'),
    path('restaurantorderpage/<city>/<name>', restaurantorderpage,name='restaurantorderpage'),
    path('restaurantinfopage/<city>/<name>', restaurantinfopage,name='restaurantinfopage'),
    path('addrestaurantreview',addrestaurantreview,name='addrestaurantreview'),
    path('restaurantloginpage',restaurantloginpage,name='restaurantloginpage'),
    path('restaurantloginaction',restaurantloginaction,name='restaurantloginaction'),
    path('restaurantlogout',restaurantlogout,name='restaurantlogout'),
    path('restaurantsettingspage',restaurantsettingspage,name='restaurantsettingspage'),
    path('restaurantsettingsaction',restaurantsettingsaction,name='restaurantsettingsaction'),
    path('restaurantchangephoto',restaurantchangephoto,name='restaurantchangephoto'),
    path('restaurantchangepasswordpage',restaurantchangepasswordpage,name='restaurantchangepasswordpage'),
    path('restaurantchangepasswordaction',restaurantchangepasswordaction,name='restaurantchangepasswordaction'),
    path('restaurantshowreviews',restaurantshowreviews,name='restaurantshowreviews'),
    path('checkorders',checkorders,name='checkorders'),
    path('changeorderstatus',changeorderstatus,name='changeorderstatus'),
    path('changedeliverystatus',changedeliverystatus,name='changedeliverystatus'),
    path('restaurantviewfooditems',restaurantviewfooditems,name='restaurantviewfooditems'),



    # menu
    path('addfooditempage', addfooditempage, name='addfooditempage'),
    path('addfooditemaction', addfooditemaction, name='addfooditemaction'),
    path('viewfooditems', viewfooditems, name='viewfooditems'),
    path('updatefooditems', updatefooditemns, name='updatefooditems'),

    #city urls
    path('addcity',addcitypage,name='addcitypage'),
    path('addcityaction',addcityaction,name='addcityaction'),
    path('viewcity',viewcity,name='viewcity'),
    path('updatecitypage',updatecitypage,name='updatecitypage'),
    path('updatecityaction',updatecityaction,name='updatecityaction'),
    path('deletecitypage', deletecitypage, name='deletecitypage'),
    path('deletecityaction', deletecityaction, name='deletecityaction'),

    #user urls
    path('deleteuser',deleteuser,name='deleteuser'),
    path('usersignupaction',usersignupaction,name='usersignupaction'),
    path('usersignuppage',usersignuppage,name='usersignuppage'),
    path('viewuserpage',viewuserpage,name='viewuserpage'),
    path('updateuserpage',updateuserpage,name='updateuserpage'),
    path('updateuseraction',updateuseraction,name='updateuseraction'),
    path('userloginapage',userloginapage,name='userloginpage'),
    path('userloginaction',userloginaction,name='userloginaction'),
    path('usersearch',usersearch,name='usersearch'),
    path('userlogoutaction',userlogoutaction,name='userlogoutaction'),
    path('addtocart',addtocart,name='addtocart'),
    path('showcartitems',showcartitems,name='showcartitems'),
    path('removecartitems',removecartitems,name='removecartitems'),
    path('checkout',checkout,name='checkout'),
    path('cart',cart,name='cart'),
    path('removeitemfromcart',removeitemfromcart,name='removeitemfromcart'),
    path('orderplace', orderplace, name='orderplace'),
    path('usershoworders', usershoworders, name='usershoworders'),
    path('usersettingspage', usersettingspage, name='usersettingspage'),
    path('usersettingsaction',usersettingsaction,name='usersettingsaction'),
    path('changeuserpicture',changeuserpicture,name='changeuserpicture'),
    path('userorderdetails', userorderdetails, name='userorderdetails'),
    path('usercheckorderstatus',usercheckorderstatus,name='usercheckorderstatus'),
    path('usertoprestaurantinweek',usertoprestaurantinweek,name='usertoprestaurantinweek'),
    path('usermostpopularrestaurants',usermostpopularrestaurants,name='usermostpopularrestaurants'),
    path('showtotalsalesbydate',showtotalsalesbydate,name='showtotalsalesbydate'),
    path('showsales',showsales,name='showsales'),
    path('uservegfooditems',uservegfooditems,name='uservegfooditems'),
    path('usernonvegfooditems',usernonvegfooditems,name='usernonvegfooditems'),
    path('test',test,name='test'),

]
