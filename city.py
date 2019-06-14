from django.shortcuts import render
from django.http import request,HttpResponse,HttpResponseRedirect
from dataqueries import *
from conversions import *

table = 'city'
database = 'foodservice'

def addcitypage(request):
    return render(request,'city/addcity.html')

def addcityaction(request):
    splitkey = '+--+==++_--'
    cityname = request.POST.get('cityname')
    status = request.POST.get('status')
    message,data = select(table,database,'cityname:'+cityname)
    if(data):
        return HttpResponse('City Aldready exists')
    else:
        valstr = cityname+splitkey+status
        message = insert_into_table(table,database,valstr,splitkey)
        return HttpResponse(message)
    #return render(request,)

def viewcity(request):
    message,data = selectall(table,database)
    if(data):
        send = tuples_to_dictionaries(data,['id','cityname','status'])
        if(send):
            return render(request,'city/viewcity.html',{'data':send})
        return HttpResponse(send)

def updatecitypage(request):

    id = request.POST.get('id')
    cityname = request.POST.get('name')
    status = request.POST.get('status')
    d = {}
    d['id'] = id
    d['cityname'] = cityname
    d['status'] = status
    return render(request,'city/updatecity.html',{'data':d})
    #return HttpResponse(message)

def updatecityaction(request):
    splitkey = "+-++-1230-++-+"
    id = request.POST.get('id')
    cityname = request.POST.get('cityname')
    status = request.POST.get('status')
    valstr = 'cityname=' + cityname + splitkey + 'status=' + status
    message = update_table(table, database, 'id:' + id, valstr, splitkey)
    return HttpResponseRedirect('viewcity')

def deletecitypage(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    status = request.POST.get('status')

    message,restdata = selectfromcolumn('restaurant',database,'city:'+id)

    restkeys = ['id','restaurantname','email','password','mobileno','address','ownername','city','status']
    citykeys = ['id','name','status']
    values = [id,name,status]
    heads = ['Id','Restaurant Name','Email','Password','Mobileno','Address','Ownername','City','Status']

    citydict = make_dictionary(citykeys,values)
    if(restdata and citydict):
        restlist = tuples_to_dictionaries(restdata,restkeys)
        return render(request, 'city/deletecity.html', {'restlist':restlist,
                        'heads':heads,'cityinfo':citydict})
    else:
        message = delete(table, database, 'id:' + id)
        return HttpResponse(message)

def deletecityaction(request):
    id = request.POST.get('id')
    message = delete(table,database,'id:'+id)
    return HttpResponse(message)