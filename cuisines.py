#Cuisines Module
from django.shortcuts import render
from django.http import *
from dataqueries import *

table='cuisine'
database = 'foodservice'

#Page Rendering Views
def insertcuisinepage(request):
    return render(request, 'cuisines/insertcuisine.html')

def updatecuisinepage(request):
    cuisineudpate = {}
    cuisineudpate['id'] = request.POST.get('id')
    cuisineudpate['cuisinename'] = request.POST.get('cuisinename')
    cuisineudpate['description'] = request.POST.get('description')
    return render(request, 'cuisines/updatecuisine.html', {'cuisinedata':cuisineudpate})

def deletecuisinepage(request):
    cuisinedelete = {}
    cuisinedelete['id'] = request.POST.get('id')
    cuisinedelete['cuisinename'] = request.POST.get('cuisinename')
    cuisinedelete['description'] = request.POST.get('description')
    return render(request,'deletecuisine.html',{'cuisinedata':cuisinedelete})

#Action Views
def viewcuisines(request):
    message,data = selectall(table,database)
    if(data is not None):
        try:
            keys = "id,cuisinename,description"
            sendabledata = TL_to_DL(data,keys)
            if(sendabledata is not None):
                return render(request, 'cuisines/viewcuisines.html', {'cuisines':sendabledata})
        except:
            return render(request, 'cuisines/viewcuisines.html')

    return render(request, 'cuisines/viewcuisines.html')

def insertcuisine(request):
    splitkey = "-+-3213+_31321-+_-_132"
    cuisinename =str(request.POST['cuisine'])
    description = str(request.POST['description'])
    values = cuisinename + splitkey + description
    if(cuisinename and description):
        message,data = select(table,database,'cuisinename:'+cuisinename)
        if(data):
            return HttpResponse('Cuisine with same name Exists')
        else:
            message = insert_into_table('cuisine', 'foodservice', values,splitkey)
    else:
        if(not (cuisinename )):
            if(not description):
                return HttpResponse('Cusinename and Description both are mandatory')
            else:
                return HttpResponse('Cuisinename is mandatory')
        else:
            return HttpResponse('Description is mandatory')
    return HttpResponseRedirect('viewcuisines')

#take tuples in a tuple and return a list of dictionaries
def TL_to_DL(tuples,keys):
    key = keys.split(",")
    sendlist = []
    if(len(tuples[0]) == len(key)):
        for tuple in tuples:
            dict = {}
            for b in range(0,len(tuple)):
                dict[key[b]] = tuple[b]
            sendlist.append(dict)
        return sendlist
    return None


def deletecuisine(request):
    id = request.POST.get('id')
    message = delete('cuisine','foodservice','id:'+id)
    return HttpResponseRedirect('viewcuisines')

def updatecuisineaction(request):
    splitkey = "++|,|++"
    id = request.POST.get('id')
    cuisinename = request.POST.get('cuisinename')
    description = request.POST.get('description')
    data = update_table(table,database,"id:"+id,"cuisinename="+cuisinename+splitkey+"description="+description,splitkey)
    return HttpResponseRedirect('viewcuisines')
