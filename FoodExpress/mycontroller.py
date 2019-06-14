from views import *
from admin import *
from index import *
from restaurant import *
from cuisines import *
from city import *
from user import *
from menu import *

from django.http import *
from django.shortcuts import render
from dataqueries import *
from conversions import *
from admin import *

database = 'foodservice'

def indexpage(request):
    if request.session.has_key('USERID'):
        return userhomepage(request)
    if request.session.has_key('ADMINID'):
        return adminhomepage(request)
    if request.session.has_key('RESTAURANTID'):
        return restauranthomepage(request)
    return render(request, 'index.html')


def showtotalsalesbydate(request):
    res = showsalesdatewise()
    return JsonResponse(res, safe=False)


def showsales(request):
    return render(request, 'admintotalsales.html')