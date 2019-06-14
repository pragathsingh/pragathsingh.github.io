from django.http import *
from django.shortcuts import *
from dataqueries import *
import os
from conversions import *
import datetime
from django.views.decorators.csrf import *

from views import *
table = 'user'
database = 'foodservice'
image_upload_path = 'static/uploads/users/'

def write_image(photo,photopath):
    photoname = str(photo)
    if not os.path.exists(photopath):
        os.mkdir(photopath)

    with open(photopath+"/"+photoname, 'wb+') as destination:
        for chunk in photo.chunks():
            destination.write(chunk)


def userhomepage(request):
    user_id = str(request.session['USERID'])
    message_1, resttuples = selectall('restaurant', database)
    message_2, fooditemstuples = selectall('menu', database)
    message_3, citiestuples = selectall('city', database)
    message_4, cuisinestuples = selectall('cuisine', database)
    message_5, categoriestuples = selectall('category', database)

    message_5, user_info = select('user', database, 'id:' + user_id)
    city_id = user_info[7]
    message_7, restaurants_in_range = selectfromcolumn('restaurant', database, 'city:' + city_id)
    rest_in_city = tuples_to_lists(restaurants_in_range)

    for index in range(0, len(rest_in_city)):
        rest_in_city[index].pop(3)

    restkeys = ['id', 'restaurantname', 'email', 'mobileno', 'address', 'ownername', 'city', 'status', 'photo']
    itemskeys = ['id', 'itemname', 'cuisinename', 'price', 'gst', 'mrp', 'photo', 'status', 'restaurantname',
                 'category', 'mark']

    restdicts = tuples_to_dictionaries(data=rest_in_city, keys=restkeys)

    return render(request, 'user/userhomepage.html', {'restaurants': restdicts})
    # return HttpResponseRedirect('userhomepage')


def usersignuppage(request):

    if not request.session.has_key('USERID'):
        message_2, cities_tuples = selectall('city', database)
        cities = [city[1] for city in cities_tuples]
        cities.sort()
        all_cities = []
        for city in cities:
            d = {}
            for c in cities_tuples:
                if city == c[1]:
                    d['id'] = c[0]
                    d['name'] = c[1]
                    break
            all_cities.append(d)
        return render(request, 'user/usersignup.html', {'cities': all_cities})
    else:
        return HttpResponseRedirect('/')

def viewuserpage(request):

    if request.session.has_key('ADMINID'):
        message, data = selectall(table, database)
        keys = ['id', 'name', 'email', 'password', 'mobileno', 'address', 'photo', 'city']
        heads = []
        for a in keys:
            heads.append(a.capitalize())

        dataindic = tuples_to_dictionaries(data, keys)
        return render(request, 'user/viewuser.html', {'data': dataindic, 'heads': heads, 'userfound': True})
    else:
        return HttpResponseRedirect('/')

def usersignupaction(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    mobileno = str(request.POST.get('mobileno'))
    address = request.POST.get('address')
    city = request.POST.get('city')
    try:
        photo = request.FILES['photo']
    except:
        photo = None

    splitkey = '++--+123+--++'
    if email and photo:
        photolocation = image_upload_path + email
        write_image(photo,photolocation)
        photolocation = photolocation[7:] + "/" + str(photo)

    if photo == None:
        photolocation = 'None'

    if username and email and password and mobileno and address and city:
        #return HttpResponse('all')

        values = username + splitkey + email + splitkey + password + splitkey + mobileno \
                     + splitkey + address + splitkey + photolocation + splitkey + city

        message,data = select(table, database, 'email:'+email)
        if(data == None):
            message = insert_into_table(table,database,values,splitkey)
            return HttpResponseRedirect('viewuserpage')

    return HttpResponseRedirect('usersignuppage')

def deleteuser(request):
    userid = request.POST.get('id')
    message = delete(table,database,'id:'+userid)

    return HttpResponseRedirect('viewuserpage')

def updateuserpage(request):
    id = request.POST.get('id')
    message, userdata = select(table, database, 'id:'+id)
    keys = ['id', 'name', 'email', 'password', 'mobileno', 'address', 'photo', 'city']
    cities = ['Amritsar', 'Jalandhar', 'Chandigarh', 'Jaipur', 'Ludhiana', 'Patiala', 'Bhatinda', 'Batala', 'Firozpur']
    cities.sort()
    #return HttpResponse(userdata)
    if(userdata):
        userlist = make_dictionary(userdata, keys)
        return render(request,'user/updateuser.html',{'user':userlist,'cities':cities})

def updateuseraction(request):
    id = request.POST.get('id')
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    mobileno = str(request.POST.get('mobileno'))
    address = request.POST.get('address')
    city = request.POST.get('city')
    try:
        photo = request.FILES['photo']
    except:
        photo = None

    splitkey = '++--+123+--++'
    if email and photo:
        photolocation = image_upload_path + email
        write_image(photo, photolocation)
        photolocation = photolocation[7:] + "/" + str(photo)

    if username and email and password and mobileno and address and city:

        if photo:
            valstr = 'name=' + username + splitkey + 'email=' + email + splitkey \
                     + 'password=' + password + splitkey + 'mobileno=' + mobileno \
                     + splitkey + 'address=' + address + splitkey + 'photo=' + photolocation \
                     + splitkey + 'city=' + city
        else:
            valstr = 'name=' + username + splitkey + 'email=' + email + splitkey \
                 + 'password=' + password + splitkey + 'mobileno=' + mobileno  \
                 + splitkey + 'address=' + address + splitkey + 'city=' + city

        message = update_table(table ,database, 'id:'+id, valstr, splitkey)
        return HttpResponseRedirect('viewuserpage')


def userloginapage(request):
    if request.session.has_key('USERID'):
        return HttpResponseRedirect('/')
    return render(request, 'user/userlogin.html')

def userloginaction(request):
    credentials = request.POST.get('signincredentials')
    password = request.POST.get('pwd')
    username = ""

    signupcomplete = False

    if '@' in credentials:
        valid = password_valid(table, database, 'password:' + password, 'email:' + credentials)
        if valid:
            message, user_info = select('user', database, 'email:' + credentials)
            user_id = user_info[0]
            user_name = user_info[1]
            user_email = user_info[2]
            user_photo = user_info[6]
    else:
        valid = password_valid(table, database, 'password:' + password, 'name:' + credentials)
        if valid:
            message, user_info = select('user', database, 'name:' + credentials)
            user_id = user_info[0]
            user_name = user_info[1]
            user_email = user_info[2]
            user_photo = user_info[6]

    if valid:
        request.session['USEREMAIL'] = user_email
        request.session['USERID'] = user_id
        request.session['USERNAME'] = user_name
        if user_photo:
            request.session['USERPHOTO'] = user_photo
        return HttpResponseRedirect('/')
        #return userhomepage(request)
    else:
        return JsonResponse({'message': 'User does not exist'})

def usersearch(request):

    search = str(request.GET.get('search'))
    search = search.lower()

    # take all data of restaurants ,citites and items for search help
    message_1, resttuples = selectall('restaurant', database)
    message_2, fooditemstuples = selectall('menu', database)
    message_3, citiestuples = selectall('city', database)
    message_4, cuisinestuples = selectall('cuisine', database)
    message_5, categoriestuples = selectall('category', database)

    # convert citiestuples to a dictionary of keys ad city id and values as their names
    citiesdict = tuple_to_onekeydic(citiestuples)
    cuisinesdict = tuple_to_onekeydic(cuisinestuples)
    restaurantdict = tuple_to_onekeydic(resttuples)
    categoriesdict = tuple_to_onekeydic(categoriestuples)

    # convert resttuples to restlists so that we can change its data
    restlists = tuples_to_lists(resttuples)
    fooditemslists = tuples_to_lists(fooditemstuples)

    for index in range(0, len(fooditemslists)):
        if fooditemslists[index][2] in cuisinesdict:
            fooditemslists[index][2] = cuisinesdict[fooditemslists[index][2]]

    restaurant_categories = []

    for index in range(0, len(restlists)):

        rest_id = str(restlists[index][0])
        tmp_categories = []
        message_6, rest_menu = selectfromcolumn('menu', database, 'restaurantid:' + rest_id)
        for item in rest_menu:
            if item[8] not in tmp_categories:
                tmp_categories.append(item[8])
        tmp_categories_name = []
        for category in tmp_categories:
            message_7, cat = select('category', database, 'id:'+str(category))
        tmp_categories_name.append(cat[1])

        restlists[index].append(tmp_categories_name)
        if restlists[index][7] in citiesdict:
            restlists[index][7] = citiesdict[restlists[index][7]]

        restlists[index].pop(3)

    resultrest = []
    resultfooditems = []
    count = 0

    for row in restlists:
        if search in row[1].lower():
            resultrest.append(restlists[count])
        count += 1
    count = 0

    for row in restlists:
        if search in row[5].lower():
            value_not_added = True
            for a in resultrest:
                if row[0] == a[0]:
                    value_not_added = False
                    break
            if value_not_added:
                resultrest.append(restlists[count])
        count += 1
    count = 0
    # return HttpResponse(fooditemslists)
    for row in fooditemslists:
        if row[8] in restaurantdict:
            rest_id = row[8]
            for restaurant in restlists:
                if rest_id == restaurant[0]:
                    fooditemslists[count].append(restaurant[6])

            fooditemslists[count][8] = restaurantdict[row[8]]

        if search in row[1].lower():
            resultfooditems.append(fooditemslists[count])
        count += 1

    restkeys = ['id', 'restaurantname', 'email', 'mobileno', 'address', 'ownername', 'city', 'status', 'photo', 'categories']
    itemskeys = ['id', 'itemname', 'cuisinename', 'price', 'gst', 'mrp', 'photo', 'status', 'restaurantname', 'category'
                    ,'mark', 'restaurantcity']
    #return HttpResponse(fooditemslists)
    restdicts = tuples_to_dictionaries(data=resultrest, keys=restkeys)
    fooditemsdicts = tuples_to_dictionaries(data=resultfooditems, keys=itemskeys)

    #return HttpResponse(restdicts)
    return render(request, 'user/usersearch.html', {'restaurants': restdicts, 'fooditems': fooditemsdicts})

def userlogoutaction(request):
    if request.session.has_key('USERID'):
        del request.session['USEREMAIL']
        del request.session['USERID']
        del request.session['USERNAME']

        has_key_1 = request.session.has_key('CARTIDS')
        if has_key_1:
            del request.session['CARTIDS']
            del request.session['CARTNAMES']
            del request.session['CARTQTY']
            del request.session['CARTAMOUNTS']

        response = {'message': 1}
    else:
        response = {'message': 0}

    return JsonResponse(response)

def restaurantorderpage(request,city,name):
    restaurant_keys = ['id', 'restaurantname', 'email', 'mobileno', 'address', 'ownername', 'city_id', 'status', 'photo', 'city_name']
    items_keys = ['id', 'itemname', 'cuisineid', 'price', 'gst', 'mrp', 'photo', 'status', 'restaurantid', 'category','mark',
                  'restaurantname', 'cuisinename', 'categoryname']

    message_1, city_data = select('city', database, 'cityname:' + city)

    if city_data:
        city_id = city_data[0]

    columns_dict = {'city': city_id, 'restaurantname': name}
    message_2, restaurant_tuple = select_from_columns('restaurant', database, columns_dict)
    restaurant_id = str(restaurant_tuple[0])
    #message_1, restaurant_tuple = select('restaurant', database, 'id:'+restaurant_id)
    message_2, cuisines_tuples = selectall('cuisine', database)
    message_3, categories_tuples = selectall('category', database)
    message_4, cities_tuples = selectall('city', database)

    restaurant_list = list(restaurant_tuple)
    restaurant_list.pop(3)

    message_5, city = select('city', database, 'id:'+str(restaurant_list[6]))
    if city:
        restaurant_list.append(city[1])

    restaurant_dict = make_dictionary(values=restaurant_list, keys=restaurant_keys)

    cuisines_dict = tuple_to_onekeydic(cuisines_tuples)
    categories_dict = tuple_to_onekeydic(categories_tuples)
    cities_dict = tuple_to_onekeydic(cities_tuples)

    message_2, food_items_tuple = selectfromcolumn('menu', database, 'restaurantid:'+restaurant_id)
    food_items_lists = tuples_to_lists(food_items_tuple)
    food_lists = list()

    for item in food_items_lists:
        tmp_list = list()

        for index in range(0, 14):
            if index < 11:
                tmp_list.append(item[index])
            else:
                if index == 11:
                    tmp_list.append(restaurant_list[1])
                if index == 12:
                    if item[2] in cuisines_dict:
                        tmp_list.append(cuisines_dict[item[2]])
                if index == 13:
                    if item[9] in categories_dict:
                        tmp_list.append(categories_dict[item[9]])
        food_lists.append(tmp_list)
    food_items_lists = food_lists
    food_items_dicts = tuples_to_dictionaries(food_items_lists, items_keys)
    #return HttpResponse(restaurant_dict)
    return render(request, 'restaurant/restaurantorder.html', {'restaurant': restaurant_dict, 'food_items':
        food_items_dicts})


def search_in_tuples_dict(data, value):
    for dict in data:
        if value == dict['id']:
            return True

    return False

def restaurantinfopage(request, city, name):

    restaurant_keys = ['id', 'restaurant_name', 'email', 'mobileno', 'address', 'ownername', 'city_id', 'status',
                       'photo', 'city_name']

    message_1, city_data = select('city', database, 'cityname:'+city)

    if city_data:
        city_id = city_data[0]

    columns_dict = {'city': city_id, 'restaurantname': name}
    message_2, restaurant = select_from_columns('restaurant', database, columns_dict)

    restaurant_list = list(restaurant)
    restaurant_list.pop(3)
    restaurant_list.append(city)
    restaurant_id = restaurant_list[0]

    restaurant_dict = make_dictionary(restaurant_list, restaurant_keys)

    message_3, food_items = selectfromcolumn('menu', database, 'restaurantid:'+str(restaurant_id))
    message_4, cuisines_tuples = selectall('cuisine', database)
    cuisines_dict = tuple_to_onekeydic(cuisines_tuples)
    cuisines_in_restaurant = list()

    for item in food_items:
        d = {}
        if item[2] in cuisines_dict:
            if not search_in_tuples_dict(cuisines_in_restaurant, item[2]):
                d['id'] = item[2]
                d['cuisine_name'] = cuisines_dict[item[2]]
                cuisines_in_restaurant.append(d)

    restaurant_pure_veg = True

    for item in food_items:
        if item[10].lower() == 'non-veg':
            restaurant_pure_veg = False
            break

    message_5, reviews = selectfromcolumn('restaurantreview', database, 'restaurantid:' + str(restaurant_list[0]))
    restaurant_rating = 0
    for review in reviews:
        if restaurant_rating == 0:
            restaurant_rating += review[3]
        else:
            restaurant_rating = (restaurant_rating + review[3])/2
    votes = len(reviews)
    rating = str(restaurant_rating)
    rating = rating[:3]

    your_rating = 0
    if request.session.has_key('USERID'):
        user_id = request.session['USERID']
        columns_dict = {'restaurantid': str(restaurant_id), 'userid': str(user_id)}
        message_2, your_review = select_from_columns('restaurantreview', database, columns_dict)

        if your_review:
            your_rating = your_review[3]

    each_user_id_list = []
    message_5, users_tuples = selectall('user', database)
    final_reviews_list = []
    for review in reviews:
        tmp = []
        for user in users_tuples:
            if review[5] == user[0]:
                tmp.append(review[2])
                tmp.append(review[3])
                tmp.append(review[4])
                tmp.append(user[1])
                tmp.append(user[6])
                break
        final_reviews_list.append(tmp)

    review_users_key = ['review', 'rating', 'datetime', 'name', 'photo']
    review_users_dict = tuples_to_dictionaries(final_reviews_list, review_users_key)

    return render(request, 'restaurant/restaurantinfo.html', {'restaurant': restaurant_dict, 'food_items': food_items,
                                                              'cuisines': cuisines_in_restaurant, 'restaurant_pure_veg':
                                                              restaurant_pure_veg, 'rating': rating, 'votes': votes,
                                                              'your_rating': your_rating, 'all_reviews':review_users_dict})

def addtocart(request):
    ids_str = request.POST.get('ids')
    names_str = request.POST.get('names')
    qty_str = request.POST.get('qty')
    amounts_str = request.POST.get('amounts')

    has_key_1 = request.session.has_key('CARTIDS')
    has_key_2 = request.session.has_key('CARTNAMES')
    has_key_3 = request.session.has_key('CARTQTY')
    has_key_4 = request.session.has_key('CARTAMOUNTS')
    if has_key_1 and has_key_2 and has_key_3 and has_key_4:
        cart_ids = request.session['CARTIDS']
        cart_names = request.session['CARTNAMES']
        cart_qty = request.session['CARTQTY']
        cart_amounts = request.session['CARTAMOUNTS']

        cart_ids_list = cart_ids.split(',')
        cart_names_list = cart_names.split(',')
        cart_qty_list = cart_qty.split(',')
        cart_amounts_list = cart_amounts.split(',')

        ids_list = ids_str.split(',')
        names_list = names_str.split(',')
        qty_list = qty_str.split(',')
        amounts_list = amounts_str.split(',')

        for index_1 in range(0, len(ids_list)):
            found = False
            for index_2 in range(0, len(cart_ids_list)):
                if ids_list[index_1] == cart_ids_list[index_2]:
                    cart_qty_list[index_2] = qty_list[index_1]
                    cart_amounts_list[index_2] = amounts_list[index_1]
                    found = True
                    break
            if not found:
                cart_ids_list.append(ids_list[index_1])
                cart_names_list.append(names_list[index_1])
                cart_qty_list.append(qty_list[index_1])
                cart_amounts_list.append(amounts_list[index_1])

        new_cart_id = ""
        new_cart_name = ""
        new_cart_qty = ""
        new_cart_amount = ""
        for index in range(0, len(cart_ids_list)):
            if index < len(cart_ids_list)-1:
                new_cart_id += cart_ids_list[index] + ","
                new_cart_name += cart_names_list[index] + ","
                new_cart_qty += cart_qty_list[index] + ","
                new_cart_amount += cart_amounts_list[index] + ","
            else:
                new_cart_id += cart_ids_list[index]
                new_cart_name += cart_names_list[index]
                new_cart_qty += cart_qty_list[index]
                new_cart_amount += cart_amounts_list[index]

        request.session['CARTIDS'] = new_cart_id
        request.session['CARTNAMES'] = new_cart_name
        request.session['CARTQTY'] = new_cart_qty
        request.session['CARTAMOUNTS'] = new_cart_amount

    else:
        request.session['CARTIDS'] = ids_str
        request.session['CARTNAMES'] = names_str
        request.session['CARTQTY'] = qty_str
        request.session['CARTAMOUNTS'] = amounts_str

    return JsonResponse({'message': 'Items Added To cart'})

def showcartitems(request):
    has_key_1 = request.session.has_key('CARTIDS')
    has_key_2 = request.session.has_key('CARTNAMES')
    has_key_3 = request.session.has_key('CARTQTY')
    has_key_4 = request.session.has_key('CARTAMOUNTS')
    if has_key_1 and has_key_2 and has_key_3 and has_key_4:
        ids = request.session['CARTIDS']
        names = request.session['CARTNAMES']
        qty = request.session['CARTQTY']
        amounts = request.session['CARTAMOUNTS']
        return JsonResponse({'ids': ids, 'names': names, 'qty': qty, 'amounts': amounts})
    return JsonResponse({'message': 'No items in cart'})

def removecartitems(request):
    has_key_1 = request.session.has_key('CARTIDS')
    has_key_2 = request.session.has_key('CARTNAMES')
    has_key_3 = request.session.has_key('CARTQTY')
    has_key_4 = request.session.has_key('CARTAMOUNTS')
    if has_key_1 and has_key_2 and has_key_3 and has_key_4:
        del request.session['CARTIDS']
        del request.session['CARTNAMES']
        del request.session['CARTQTY']
        del request.session['CARTAMOUNTS']
        return JsonResponse({'message': 'Items Deleted from cart'})
    return JsonResponse({'message': 'No Items in cart'})

def checkout(request):

    if request.session.has_key('USERID'):

        user_id = request.session['USERID']
        has_key_1 = request.session.has_key('CARTIDS')
        has_key_2 = request.session.has_key('CARTNAMES')
        has_key_3 = request.session.has_key('CARTQTY')
        has_key_4 = request.session.has_key('CARTAMOUNTS')
        if has_key_1 and has_key_2 and has_key_3 and has_key_4:
            cart_ids = request.session['CARTIDS']
            cart_names = request.session['CARTNAMES']
            cart_qty = request.session['CARTQTY']
            cart_amounts = request.session['CARTAMOUNTS']

            cart_ids_list = cart_ids.split(',')
            cart_names_list = cart_names.split(',')
            cart_qty_list = cart_qty.split(',')
            cart_amounts_list = cart_amounts.split(',')

            if cart_ids == '':
                del request.session['CARTIDS']
                del request.session['CARTNAMES']
                del request.session['CARTQTY']
                del request.session['CARTAMOUNTS']
                return HttpResponse('All items from cart was deleted')

            total_amount = 0
            for amount in cart_amounts_list:
                total_amount += int(amount)

            message_1, items_tuple = selectall('menu', database)
            mark_id_lists = []
            cart_items_mrp = list()
            for cart in cart_ids_list:
                for ind in items_tuple:
                    if int(cart) == ind[0]:
                        mark_id_lists.append(ind[10])
                        cart_items_mrp.append(ind[5])

            cart_items = list()
            for index in range(0, len(cart_ids_list)):
                cart_items_dict = dict()
                cart_items_dict['id'] = cart_ids_list[index]
                cart_items_dict['name'] = cart_names_list[index]
                cart_items_dict['qty'] = cart_qty_list[index]
                cart_items_dict['mrp'] = cart_items_mrp[index]
                cart_items_dict['amount'] = cart_amounts_list[index]
                cart_items_dict['mark'] = mark_id_lists[index]
                cart_items.append(cart_items_dict)

            message_2, user = select(table, database, 'id:'+str(user_id))
            user_info = list(user)
            user_info.pop(3)
            user_keys = ['id', 'name', 'email', 'mobileno', 'address', 'photo', 'city']

            user_dict = make_dictionary(user_info, user_keys)

            return render(request, 'user/order.html', {'user': user_dict, 'cart_items': cart_items, 'totalamount': total_amount})

        return JsonResponse({'message': 'cart is empty'})

    return JsonResponse({'message': 'no user loged in'})

def removeitemfromcart(request):

    item_id = request.POST.get('id')
    has_key_1 = request.session.has_key('CARTIDS')
    has_key_2 = request.session.has_key('CARTNAMES')
    has_key_3 = request.session.has_key('CARTQTY')
    has_key_4 = request.session.has_key('CARTAMOUNTS')
    if has_key_1 and has_key_2 and has_key_3 and has_key_4:
        cart_ids = request.session['CARTIDS']
        cart_names = request.session['CARTNAMES']
        cart_qty = request.session['CARTQTY']
        cart_amounts = request.session['CARTAMOUNTS']

        cart_ids_list = cart_ids.split(',')
        cart_names_list = cart_names.split(',')
        cart_qty_list = cart_qty.split(',')
        cart_amounts_list = cart_amounts.split(',')
        item_index = 0
        for index in range(0, len(cart_ids_list)):
            if id == cart_ids_list[index]:
                item_index = index
                break

        cart_ids_list.pop(item_index)
        cart_names_list.pop(item_index)
        cart_qty_list.pop(item_index)
        cart_amounts_list.pop(item_index)

        new_cart_id = ""
        new_cart_name = ""
        new_cart_qty = ""
        new_cart_amount = ""

        for index in range(0, len(cart_ids_list)):
            if index < len(cart_ids_list) - 1:
                new_cart_id += cart_ids_list[index] + ","
                new_cart_name += cart_names_list[index] + ","
                new_cart_qty += cart_qty_list[index] + ","
                new_cart_amount += cart_amounts_list[index] + ","
            else:
                new_cart_id += cart_ids_list[index]
                new_cart_name += cart_names_list[index]
                new_cart_qty += cart_qty_list[index]
                new_cart_amount += cart_amounts_list[index]

        request.session['CARTIDS'] = new_cart_id
        request.session['CARTNAMES'] = new_cart_name
        request.session['CARTQTY'] = new_cart_qty
        request.session['CARTAMOUNTS'] = new_cart_amount

        return JsonResponse({'message': 'Item removed from cart'})
    return JsonResponse({'message': 'There are no items in cart'})

@csrf_exempt
def orderplace(request):
    if request.session.has_key('USERID'):

        user_id = request.session['USERID']
        #return JsonResponse({'message': 'user exists'})
        has_key_1 = request.session.has_key('CARTIDS')
        has_key_2 = request.session.has_key('CARTNAMES')
        has_key_3 = request.session.has_key('CARTQTY')
        has_key_4 = request.session.has_key('CARTAMOUNTS')
        if has_key_1 and has_key_2 and has_key_3 and has_key_4:

            cart_ids = request.session['CARTIDS']
            cart_names = request.session['CARTNAMES']
            cart_qty = request.session['CARTQTY']
            cart_amounts = request.session['CARTAMOUNTS']

            cart_ids_list = cart_ids.split(',')
            cart_names_list = cart_names.split(',')
            cart_qty_list = cart_qty.split(',')
            cart_amounts_list = cart_amounts.split(',')
            #return JsonResponse({'message': 'cart has items'})
            if cart_ids == '':
                del request.session['CARTIDS']
                del request.session['CARTNAMES']
                del request.session['CARTQTY']
                del request.session['CARTAMOUNTS']
                #return JsonResponse({'message', 'There was not any item in cart'})
                #return HttpResponse('There was not any item in cart')

            else:
                date_of_order = datetime.datetime.now()
                message_1, all_items = selectall('menu', database)
                message_2, user = select(table, database, 'id:' + str(user_id))

                useremail = user[2]
                username = user[1]
                mobileno = user[4]
                deliveryaddress = user[5]
                city = user[7]
                paymentmode = request.POST.get('paymentmode')

                orderstatus = "not-accepted"
                deliverystatus = "not-delivered"
                if paymentmode == 'cod':
                    paymentstatus = "not-paid"
                else:
                    paymentstatus = "paid"

                items_in_cart = list()
                for index_1 in range(0, len(cart_ids_list)):
                    for index_2 in range(0, len(all_items)):

                        if int(cart_ids_list[index_1]) == all_items[index_2][0]:
                            tmp = list(all_items[index_2])
                            tmp.append(cart_qty_list[index_1])
                            tmp.append(cart_amounts_list[index_1])
                            items_in_cart.append(tmp)
                            break
                restaurant_info = dict()

                for item in items_in_cart:
                    if item[8] not in restaurant_info:
                        restaurant_info[item[8]] = list()
                        restaurant_info[item[8]].append(item)
                    else:
                        restaurant_info[item[8]].append(item)
                show = ""
                current_order_ids = []
                for key, value in restaurant_info.items():
                    total = 0.0
                    for v in value:
                        total += float(v[12])

                    splitkey = '--_***_++'

                    ins_value = str(user_id) + splitkey + useremail + splitkey + username + splitkey +\
                                 mobileno + splitkey + city + splitkey + deliveryaddress + splitkey + str(total) +\
                                 splitkey + str(date_of_order) + splitkey + str(key) + splitkey + paymentmode

                    message_3 = insert_into_table('ordertable', database, ins_value, splitkey)

                    check_date = str(date_of_order)
                    dot_index = check_date.find('.')
                    check_date = check_date[:dot_index]
                    d = {'userid': user_id, 'dateoforder': str(check_date), 'restaurantid': str(key)}
                    message_4, order_table = select_from_columns('ordertable', database, d)
                    order_id = order_table[0]
                    current_order_ids.append(order_id)

                    order_status_values = str(order_id) + splitkey + orderstatus + splitkey + deliverystatus\
                                           + splitkey + paymentstatus
                    message_5 = insert_into_table('orderstatus', database, order_status_values, splitkey)

                    for v in value:
                        insert = str(order_id) + splitkey + str(v[0]) + splitkey + v[1] + splitkey + str(v[5]) +\
                                 splitkey + str(v[11]) + splitkey + str(v[12])
                        insert_into_table('orderdetail', database, insert, splitkey)

                    del request.session['CARTIDS']
                    del request.session['CARTNAMES']
                    del request.session['CARTQTY']
                    del request.session['CARTAMOUNTS']

                    return JsonResponse({'message': 'Order was made', 'order_ids': current_order_ids})

    return JsonResponse({'message': 'Order not made'})
    #return HttpResponseRedirect('')


def userorderdetails(request):
    if request.session.has_key('USERID'):
        new_order_ids_str = request.POST.get('neworderids')
        new_order_ids = new_order_ids_str.split(',')
        all_orders = []
        for id in new_order_ids:
            message_1, ordertable = select('ordertable', database, 'id:'+id)
            rest_id = ordertable[9]
            message_2, rest_info = select('restaurant', database, 'id:'+str(rest_id))
            rest_name = rest_info[1]
            rest_address = rest_info[5]

            message_3, order_status_tuple = select('orderstatus', database, 'orderid:' + id)
            order_status = list(order_status_tuple)
            order_status.pop(0)
            order_status.pop(0)
            order_dict = dict()
            order_dict['order_id'] = id
            order_dict['orderstatus'] = order_status[0]
            order_dict['deliverystatus'] = order_status[1]
            order_dict['paymentstatus'] = order_status[2]
            order_dict['restaurantname'] = rest_name
            order_dict['restaurantaddress'] = rest_address
            order_dict['amount'] = ordertable[7]
            message_4,order_items_tuple = selectfromcolumn('orderdetail', database, 'orderid:'+id)

            order_items = tuples_to_lists(order_items_tuple)
            for index in range(0, len(order_items)):
                order_items[index].pop(0)
                order_items[index].pop(0)
                order_items[index].pop(0)

            order_items_dict = tuples_to_dictionaries(order_items, ['itemname', 'price', 'qty', 'amount'])
            order_dict['orderitems'] = order_items_dict
            all_orders.append(order_dict)

        request.session['ORDERIDS'] = new_order_ids_str

        return render(request, 'user/userorderdetails.html', {'orders': all_orders, 'order_ids': new_order_ids_str})

def usercheckorderstatus(request):
    #order_ids_str = request.POST.get('order_id')
    if request.session.has_key('ORDERIDS'):
        order_ids_str = request.session['ORDERIDS']
        order_ids = order_ids_str.split(',')
        all_stats = []
        for id in order_ids:

            message, order_status = select('orderstatus', database, 'orderid:'+id)
            orderstat = order_status[2]
            deliverystat = order_status[3]
            paymentstat = order_status[4]

            tmp_dict = dict()
            tmp_dict['id'] = id
            tmp_dict['orderstatus'] = orderstat
            tmp_dict['deliverystatus'] = deliverystat
            tmp_dict['paymentstatus'] = paymentstat
            all_stats.append(tmp_dict)
        return JsonResponse({'message': 1, 'all_stats': all_stats})
    return JsonResponse({'message': 0})


def cart(request):

    if request.session.has_key('USERID'):

        user_id = request.session['USERID']
        has_key_1 = request.session.has_key('CARTIDS')
        has_key_2 = request.session.has_key('CARTNAMES')
        has_key_3 = request.session.has_key('CARTQTY')
        has_key_4 = request.session.has_key('CARTAMOUNTS')
        if has_key_1 and has_key_2 and has_key_3 and has_key_4:
            cart_ids = request.session['CARTIDS']
            cart_names = request.session['CARTNAMES']
            cart_qty = request.session['CARTQTY']
            cart_amounts = request.session['CARTAMOUNTS']

            cart_ids_list = cart_ids.split(',')
            cart_names_list = cart_names.split(',')
            cart_qty_list = cart_qty.split(',')
            cart_amounts_list = cart_amounts.split(',')

            if cart_ids == '':
                del request.session['CARTIDS']
                del request.session['CARTNAMES']
                del request.session['CARTQTY']
                del request.session['CARTAMOUNTS']
                return render(request, 'user/cart.html', {'data': 'null'})

            else:

                message_1, items_tuple = selectall('menu', database)
                mark_id_lists = []
                cart_items_mrp = list()
                for cart in cart_ids_list:
                    for ind in items_tuple:
                        if int(cart) == ind[0]:
                            mark_id_lists.append(ind[10])
                            cart_items_mrp.append(ind[5])

                cart_items = list()
                for index in range(0, len(cart_ids_list)):
                    cart_items_dict = dict()
                    cart_items_dict['id'] = cart_ids_list[index]
                    cart_items_dict['name'] = cart_names_list[index]
                    cart_items_dict['qty'] = cart_qty_list[index]
                    cart_items_dict['mrp'] = cart_items_mrp[index]
                    cart_items_dict['amount'] = cart_amounts_list[index]
                    cart_items_dict['mark'] = mark_id_lists[index]
                    cart_items.append(cart_items_dict)

                return render(request, 'user/cart.html', {'cart_items': cart_items})
        return render(request, 'user/cart.html')

    return HttpResponseRedirect('')

def usershoworders(request):

    if request.session.has_key('USERID'):

        user_id = str(request.session['USERID'])
        message_1, order_table = selectfromcolumn('ordertable', database, 'userid:'+user_id)

        order_items = list()
        #return HttpResponse(order_table)
        for order in order_table:

            order_id = str(order[0])
            restaurant_id = str(order[9])
            delivery_address = order[6]
            dateoforder = order[8]
            payment_mode = order[10]
            amount = order[7]

            message_3, restaurant_info = select('restaurant', database, 'id:'+restaurant_id)
            city_id = str(restaurant_info[7])
            rest_name = restaurant_info[1]
            rest_address = restaurant_info[5]


            restaurant_name = restaurant_info[1]
            message_4, city_info = select('city', database, 'id:' + city_id)
            city_name = city_info[1]

            message_2, order_details_tuples = selectfromcolumn('orderdetail', database, 'orderid:'+order_id)
            order_details = list()

            for order in order_details_tuples:
                order_details.append(list(order))

            for index in range(0, len(order_details)):

                item_id = order_details[index][2]
                message_5, item_info = select('menu', database, 'id:'+str(item_id))
                photo = item_info[6]
                mark = item_info[10]
                order_details[index].append(restaurant_id)
                order_details[index].append(restaurant_name)
                order_details[index].append(city_name)
                order_details[index].append(photo)
                order_details[index].append(mark)

            keys = ['id', 'orderid', 'itemid', 'itemname', 'mrp', 'qty', 'amount',
                    'restaurantid', 'restaurantname', 'restaurantcity', 'photo', 'mark']

            data = tuples_to_dictionaries(order_details, keys=keys)
            tmp_list = list()
            tmp_list.append(data)
            tmp_dict = {'amount': amount, 'dateoforder': dateoforder, 'delivery_address': delivery_address,'payment_mode': payment_mode,
                        'orders': data,'orderid': order_id,'restaurantname':rest_name,'restaurantaddress':rest_address}
            order_items.append(tmp_dict)

        return render(request, 'user/usershoworders.html', {'all_orders': order_items})
    return render(request, 'user/usershoworders.html')

def usersettingspage(request):

    if request.session.has_key('USERID'):
        user_id = request.session['USERID']
        message, userdata = select(table, database, 'id:' + str(user_id))
        keys = ['id', 'name', 'email', 'password', 'mobileno', 'address', 'photo', 'city']
        message_2, cities_tuples = selectall('city', database)
        cities = [city[1] for city in cities_tuples]
        cities.sort()

        if userdata:
            userlist = make_dictionary(userdata, keys)
            return render(request, 'user/usersettings.html', {'user': userlist, 'cities': cities})

def usersettingsaction(request):

    id = request.POST.get('id')
    username = request.POST.get('username')
    password = request.POST.get('password')
    mobileno = str(request.POST.get('mobileno'))
    address = request.POST.get('address')
    city = request.POST.get('city')

    splitkey = '++--+123+--++'

    if request.session.has_key('USERNAME'):
        request.session['USERNAME'] = username

    if username and password and mobileno and address and city:
        valstr = 'name=' + username + splitkey + 'password=' + password + splitkey + 'mobileno=' + mobileno  \
                  + splitkey + 'address=' + address + splitkey + 'city=' + city

        message = update_table(table, database, 'id:'+id, valstr, splitkey)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('usersettingsaction')

def changeuserpicture(request):
    ''

def usermostpopularrestaurants(request):
    if request.session.has_key('USERID'):
        user_id = str(request.session["USERID"])
        message_1, user_info = select('user', database, 'id:'+user_id)
        user_city = user_info[7]
        message_4, city_info = select('city', database, 'id:'+user_city)
        city_name = city_info[1]
        message_2, restaurants_tuple = selectfromcolumn('restaurant', database, 'city:'+str(user_city))
        week_order_rests = {}
        for restaurant in restaurants_tuple:
            message_3, rest_orders = selectfromcolumn('ordertable', database, 'restaurantid:'+str(restaurant[0]))
            # if there are any orders then
            if rest_orders:
                week_order_rests[len(rest_orders)] = restaurant[0]

        sorted_rest = sorted(week_order_rests.items(), reverse=True)
        rests_ids = list()
        for info in sorted_rest:
            rests_ids.append(info[1])

        final_rests = []
        for id in rests_ids:
            for index in range(0, len(restaurants_tuple)):
                if id == restaurants_tuple[index][0]:
                    if restaurants_tuple[index][8] == 'Approved':
                        final_rests.append(list(restaurants_tuple[index]))
                    break

        for index in range(0, len(final_rests)):
            rest_id = str(final_rests[index][0])
            final_rests[index].pop(3)
            final_rests[index].pop(2)
            final_rests[index].pop(4)
            final_rests[index].pop(5)
            final_rests[index].append(city_name)
            final_rests[index].pop(0)
            final_rests[index].pop(1)
            final_rests[index].pop(2)

            rating = 0
            message_5, review_info = selectfromcolumn('restaurantreview', database, 'restaurantid:'+rest_id)
            if review_info:
                for review in review_info:
                    rating += review[3]
                rating = rating/len(review_info)
                final_rests[index].append(rating)
        #return HttpResponse(final_rests)
        restaurant_keys = ['restaurantname', 'address', 'photo', 'cityname', 'rating']
        restaurant_dict = tuples_to_dictionaries(final_rests, restaurant_keys)
        #return HttpResponse(restaurant_dict)
        return render(request, 'user/popularrestaurants.html', {'restaurants': restaurant_dict})

def usertoprestaurantinweek(request):
    ''

def uservegfooditems(request):

    # take all data of restaurants ,citites and items for search help
    message_1, resttuples = selectall('restaurant', database)
    message_2, fooditemstuples = selectall('menu', database)
    message_3, citiestuples = selectall('city', database)
    message_4, cuisinestuples = selectall('cuisine', database)
    message_5, categoriestuples = selectall('category', database)

    # convert citiestuples to a dictionary of keys ad city id and values as their names
    citiesdict = tuple_to_onekeydic(citiestuples)
    cuisinesdict = tuple_to_onekeydic(cuisinestuples)
    restaurantdict = tuple_to_onekeydic(resttuples)
    categoriesdict = tuple_to_onekeydic(categoriestuples)

    # convert resttuples to restlists so that we can change its data
    restlists = tuples_to_lists(resttuples)
    fooditemslists = tuples_to_lists(fooditemstuples)

    for index in range(0, len(fooditemslists)):
        if fooditemslists[index][2] in cuisinesdict:
            fooditemslists[index][2] = cuisinesdict[fooditemslists[index][2]]

    restaurant_categories = []

    for index in range(0, len(restlists)):

        rest_id = str(restlists[index][0])
        tmp_categories = []
        message_6, rest_menu = selectfromcolumn('menu', database, 'restaurantid:' + rest_id)
        for item in rest_menu:
            if item[8] not in tmp_categories:
                tmp_categories.append(item[8])
        tmp_categories_name = []
        for category in tmp_categories:
            message_7, cat = select('category', database, 'id:' + str(category))
        tmp_categories_name.append(cat[1])

        restlists[index].append(tmp_categories_name)
        if restlists[index][7] in citiesdict:
            restlists[index][7] = citiesdict[restlists[index][7]]

        restlists[index].pop(3)

    resultrest = []
    resultfooditems = []
    count = 0

    # return HttpResponse(fooditemslists)
    for row in fooditemslists:
        if row[8] in restaurantdict:
            rest_id = row[8]
            for restaurant in restlists:
                if rest_id == restaurant[0]:
                    fooditemslists[count].append(restaurant[6])

            fooditemslists[count][8] = restaurantdict[row[8]]

        if 'veg' == row[10].lower():
            resultfooditems.append(fooditemslists[count])
        count += 1
    #return HttpResponse(resultfooditems)
    restkeys = ['id', 'restaurantname', 'email', 'mobileno', 'address', 'ownername', 'city', 'status', 'photo',
                'categories']
    itemskeys = ['id', 'itemname', 'cuisinename', 'price', 'gst', 'mrp', 'photo', 'status', 'restaurantname', 'category'
        , 'mark', 'restaurantcity']
    # return HttpResponse(fooditemslists)
    restdicts = tuples_to_dictionaries(data=resultrest, keys=restkeys)
    fooditemsdicts = tuples_to_dictionaries(data=resultfooditems, keys=itemskeys)

    # return HttpResponse(restdicts)
    return render(request, 'user/showvegitems.html', {'restaurants': restdicts, 'fooditems': fooditemsdicts})


def usernonvegfooditems(request):
    # take all data of restaurants ,citites and items for search help
    message_1, resttuples = selectall('restaurant', database)
    message_2, fooditemstuples = selectall('menu', database)
    message_3, citiestuples = selectall('city', database)
    message_4, cuisinestuples = selectall('cuisine', database)
    message_5, categoriestuples = selectall('category', database)

    # convert citiestuples to a dictionary of keys ad city id and values as their names
    citiesdict = tuple_to_onekeydic(citiestuples)
    cuisinesdict = tuple_to_onekeydic(cuisinestuples)
    restaurantdict = tuple_to_onekeydic(resttuples)
    categoriesdict = tuple_to_onekeydic(categoriestuples)

    # convert resttuples to restlists so that we can change its data
    restlists = tuples_to_lists(resttuples)
    fooditemslists = tuples_to_lists(fooditemstuples)

    for index in range(0, len(fooditemslists)):
        if fooditemslists[index][2] in cuisinesdict:
            fooditemslists[index][2] = cuisinesdict[fooditemslists[index][2]]

    restaurant_categories = []

    for index in range(0, len(restlists)):

        rest_id = str(restlists[index][0])
        tmp_categories = []
        message_6, rest_menu = selectfromcolumn('menu', database, 'restaurantid:' + rest_id)
        for item in rest_menu:
            if item[8] not in tmp_categories:
                tmp_categories.append(item[8])
        tmp_categories_name = []
        for category in tmp_categories:
            message_7, cat = select('category', database, 'id:' + str(category))
        tmp_categories_name.append(cat[1])

        restlists[index].append(tmp_categories_name)
        if restlists[index][7] in citiesdict:
            restlists[index][7] = citiesdict[restlists[index][7]]

        restlists[index].pop(3)

    resultrest = []
    resultfooditems = []
    count = 0

    for row in fooditemslists:
        if row[8] in restaurantdict:
            rest_id = row[8]
            for restaurant in restlists:
                if rest_id == restaurant[0]:
                    fooditemslists[count].append(restaurant[6])

            fooditemslists[count][8] = restaurantdict[row[8]]

        if 'non-veg' == row[10].lower():
            resultfooditems.append(fooditemslists[count])
        count += 1
    # return HttpResponse(resultfooditems)
    restkeys = ['id', 'restaurantname', 'email', 'mobileno', 'address', 'ownername', 'city', 'status', 'photo',
                'categories']
    itemskeys = ['id', 'itemname', 'cuisinename', 'price', 'gst', 'mrp', 'photo', 'status', 'restaurantname', 'category'
        , 'mark', 'restaurantcity']
    # return HttpResponse(fooditemslists)
    restdicts = tuples_to_dictionaries(data=resultrest, keys=restkeys)
    fooditemsdicts = tuples_to_dictionaries(data=resultfooditems, keys=itemskeys)

    # return HttpResponse(restdicts)
    return render(request, 'user/nonvegitems.html', {'restaurants': restdicts, 'fooditems': fooditemsdicts})


def test(request):
    return JsonResponse({'message':'Pragath is g8'})