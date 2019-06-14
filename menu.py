from dataqueries import *
import os
from conversions import *
from django.shortcuts import render, HttpResponseRedirect

table = 'menu'
database = 'foodservice'

image_upload_path = 'static/uploads/restaurants/fooditems/'

def write_image(photo,photopath,itemname):
    photoname = str(photo)

    if not os.path.exists(photopath):
        os.mkdir(photopath)

    photopath += ("/" + itemname)

    if not os.path.exists(photopath):
        os.mkdir(photopath)

    with open(photopath+"/"+photoname, 'wb+') as destination:
        for chunk in photo.chunks():
            destination.write(chunk)
    return photopath

def addfooditempage(request):

    if request.session.has_key('RESTAURANTID'):

        message_1, cuisinesdata = selectall('cuisine', database)
        message_2, categories_tuples = selectall('category', database)
        categories_lists = tuples_to_lists(categories_tuples)
        categories_dicts = tuples_to_dictionaries(categories_lists, ['id', 'name'])

        cuisines = list()
        for row in cuisinesdata:
            d = {}
            d['id'] = row[0]
            d['name'] = row[1]
            cuisines.append(d)

        return render(request, 'menu/addfooditem.html', {'cuisines': cuisines, 'categories': categories_dicts})
    return HttpResponseRedirect('/')

def addfooditemaction(request):

    if request.session.has_key('RESTAURANTID'):
        item_exists = False
        restaurantid = str(request.session['RESTAURANTID'])
        cuisienid = request.POST.get('cuisineid')
        itemname = request.POST.get('itemname')
        category_id = request.POST.get('category_id')
        price = request.POST.get('price')
        gst = request.POST.get('gst')
        mrp = request.POST.get('mrp')
        status = request.POST.get('status')
        mark = request.POST.get('mark')

        try:
            photo = request.FILES['photo']
        except:
            photo = None
        #return HttpResponse(restaurantid)
        splitkey = '++'
        if restaurantid and photo:
            photolocation = image_upload_path + restaurantid
            photolocation = write_image(photo, photolocation, itemname)
            photolocation = photolocation[7:] + "/" + str(photo)

        if photo == None:
            photolocation = 'None'

        if restaurantid and cuisienid and itemname and category_id and price and gst and mrp and status and mark:
            # return HttpResponse('all')

            values = itemname + splitkey + cuisienid + splitkey + price + splitkey + gst \
                     + splitkey + mrp + splitkey + photolocation + splitkey + status \
                     + splitkey + restaurantid + splitkey + category_id + splitkey + mark.lower()

            message, data = selectfromcolumn('menu', database, 'restaurantid:'+restaurantid)
            itemnamelower = itemname.lower()
            for row in data:
                tmp = row[1].lower()
                if tmp == itemnamelower:
                    item_exists = True

            if not item_exists:
                message = insert_into_table('menu', database, values, splitkey)
                return HttpResponseRedirect('restaurantviewfooditems')

    return HttpResponseRedirect('/')

def restaurantviewfooditems(request):
    if request.session.has_key('RESTAURANTID'):
        rest_id = str(request.session['RESTAURANTID'])
        message_1, fooditemsdata = selectfromcolumn(table, database, 'restaurantid:'+rest_id)
        message_3, cuisinedata = selectall('cuisine', database)
        message_4, categories_tuples = selectall('category', database)
        categories_dict = tuple_to_onekeydic(categories_tuples)
        # return HttpResponse(restaurant_dict)
        heads = ['Id', 'Item Name', 'Cuisine', 'Price', 'Gst', 'Mrp', 'Photo', 'Status', 'Category', 'Veg/Non-Veg']

        keys = ['id', 'itemname', 'cuisinename', 'price', 'gst', 'mrp', 'photo', 'status', 'category', 'mark']
        if fooditemsdata:
            fooditems = tuples_to_lists(fooditemsdata)
            for index in range(0, len(fooditems)):
                if fooditems[index][9] in categories_dict:
                    fooditems[index][9] = categories_dict[fooditems[index][9]]

            for index in range(0, len(fooditems)):
                for restindex in range(0, len(cuisinedata)):
                    if fooditems[index][2] == cuisinedata[restindex][0]:
                        fooditems[index][2] = cuisinedata[restindex][1]
                        break

            for index in range(0, len(fooditems)):
                fooditems[index].pop(8)

            foods = tuples_to_dictionaries(fooditems, keys)
            return render(request, 'menu/viewfooditems.html', {'fooditems': foods, 'heads': heads})

def viewfooditems(request):
    message_1, fooditemsdata = selectall(table, database)
    message_2, restaurantdata = selectall('restaurant', database)
    message_3, cuisinedata = selectall('cuisine', database)
    message_4, categories_tuples = selectall('category', database)
    categories_dict = tuple_to_onekeydic(categories_tuples)
    restaurant_dict = tuple_to_onekeydic(restaurantdata)
    #return HttpResponse(restaurant_dict)
    heads = ['Id', 'Item Name', 'Cuisine', 'Price', 'Gst', 'Mrp', 'Restaurantname','Photo', 'Status', 'Category', 'Veg/Non-Veg']

    keys = ['id', 'itemname', 'cuisinename', 'price', 'gst', 'mrp', 'photo', 'status', 'restaurantname', 'category', 'mark']
    if fooditemsdata:
        fooditems = tuples_to_lists(fooditemsdata)
        #fooditems = tuples_to_dictionaries(fooditemsdata,keys)
        for index in range(0, len(fooditems)):

            if fooditems[index][9] in categories_dict:
                fooditems[index][9] = categories_dict[fooditems[index][9]]

            if fooditems[index][8] in restaurant_dict:
                fooditems[index][8] = restaurant_dict[fooditems[index][8]]

        for index in range(0, len(fooditems)):
            for restindex in range(0, len(restaurantdata)):
                if fooditems[index][8] == restaurantdata[restindex][0]:
                    fooditems[index][8] = restaurantdata[restindex][1]
                    break


        for index in range(0, len(fooditems)):
            for restindex in range(0, len(cuisinedata)):
                if fooditems[index][2] == cuisinedata[restindex][0]:
                    fooditems[index][2] = cuisinedata[restindex][1]
                    break

        foods = tuples_to_dictionaries(fooditems,keys)
        return render(request, 'menu/viewfooditems.html', {'fooditems':foods,'heads':heads})

def updatefooditemns(request):
    ''