from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from dataqueries import *
from conversions import *
import os
import shutil
import datetime

table = 'restaurant'
database = 'foodservice'

def restaurantshoworders(request):
    if request.session.has_key('RESTAURANTID'):
        rest_id = str(request.session['RESTAURANTID'])

        message, orders_tuples = selectfromcolumn('ordertable', database, 'restaurantid:' + rest_id)
        orders_length = len(orders_tuples)
        dates = [order[8] for order in orders_tuples]
        dates.sort(reverse=True)

        new = []
        for date in dates:
            for order in orders_tuples:
                if date == order[8]:
                    new.append(list(order))

        order_details = []
        for order in new:
            tmp_1 = []
            order_id = str(order[0])
            message_2, item_info = selectfromcolumn('orderdetail', database, 'orderid:' + order_id)
            for item in item_info:
                tmp_2 = list()
                tmp_2.append(item[3])
                tmp_2.append(item[4])
                tmp_2.append(item[5])
                tmp_2.append(item[6])
                tmp_1.append(tmp_2)

            order_details.append(tmp_1)

        item_keys = ['itemname', 'price', 'qty', 'amount']
        item_lists = []
        for order in order_details:
            items_dicts = tuples_to_dictionaries(order, item_keys)
            item_lists.append(items_dicts)

        orders_refined = list()
        order_ids = list()
        for order in new:
            order_ids.append(order[0])
            order.pop(0)
            order.pop(0)
            order.pop(0)
            order.pop(6)
            orders_refined.append(order)
        count = 0
        final_orders = []
        for order in orders_refined:
            message_3, order_status = select('orderstatus', database, 'orderid:' + str(order[0]))
            # if order_status[3] == 'not delivered' or order_status[4] == 'not paid' or order_status[2] == 'not started':
            keys = ['name', 'mobileno', 'city', 'deliveryaddress', 'amount', 'dateoforder', 'paymentmode']
            tmp = make_dictionary(order, keys)
            tmp['items'] = item_lists[count]
            final_orders.append(tmp)
            count += 1
        ids_str = ""
        count = 0
        for ids in order_ids:
            if count < len(order_ids) - 1:
                ids_str += str(ids) + ","
            else:
                ids_str += str(ids)
            count += 1

        return render(request, 'restaurant/restauranthomepage.html', {'orders': final_orders, 'order_ids': ids_str})
    else:
        return HttpResponseRedirect('/')


def restauranthomepage(request):
    if request.session.has_key('RESTAURANTID'):
        rest_id = str(request.session['RESTAURANTID'])

        message, orders_tuples = selectfromcolumn('ordertable', database, 'restaurantid:'+rest_id)
        orders_length = len(orders_tuples)
        dates = list()
        for order in orders_tuples:
            message_3, order_status = select('orderstatus', database, 'orderid:' + str(order[0]))
            if order_status[3] == 'not-delivered' or order_status[4] == 'not-paid' or order_status[2] == 'not-accepted':
                dates.append(order[8])

        dates.sort(reverse=True)

        new = []
        for date in dates:
            for order in orders_tuples:
                if date == order[8]:
                    new.append(list(order))

        order_details = []
        for order in new:
            tmp_1 = []
            order_id = str(order[0])
            message_2, item_info = selectfromcolumn('orderdetail', database, 'orderid:'+order_id)

            for item in item_info:
                tmp_2 = list()
                tmp_2.append(item[3])
                tmp_2.append(item[4])
                tmp_2.append(item[5])
                tmp_2.append(item[6])
                tmp_1.append(tmp_2)

            order_details.append(tmp_1)

        item_keys = ['itemname', 'price', 'qty', 'amount']
        item_lists = []
        for order in order_details:
            items_dicts = tuples_to_dictionaries(order, item_keys)
            item_lists.append(items_dicts)

        orders_refined = list()
        order_ids = list()
        for order in new:
            order_ids.append(order[0])
            message_3, order_status = select('orderstatus', database, 'orderid:' + str(order[0]))
            order.append(order_status[0])
            order.append(order_status[2])
            order.append(order_status[3])
            order.append(order_status[4])

            order.pop(1)
            order.pop(1)
            order.pop(7)
            orders_refined.append(order)
        count = 0
        final_orders = []
        for order in orders_refined:

            keys = ['id', 'name', 'mobileno', 'city', 'deliveryaddress', 'amount', 'dateoforder', 'paymentmode',
                    'statusid', 'orderstatus', 'deliverystatus', 'paymentstatus']
            tmp = make_dictionary(order, keys)
            tmp['items'] = item_lists[count]
            final_orders.append(tmp)
            count += 1
        ids_str = ""
        count = 0
        for ids in order_ids:
            if count < len(order_ids) - 1:
                ids_str += str(ids) + ","
            else:
                ids_str += str(ids)
            count += 1

        return render(request, 'restaurant/restauranthomepage.html', {'orders': final_orders, 'order_ids': ids_str})
    else:
        return HttpResponseRedirect('/')


def changeorderstatus(request):
    if request.session.has_key('RESTAURANTID'):
        id = request.POST.get('order_id')
        splitkey = "--+23+--"
        values = "orderstatus=accepted"
        message_1, success = update_table('orderstatus', database, 'id:'+str(id), values, splitkey)
        if success == 1:
            return JsonResponse({'message': 1})
        else:
            return JsonResponse({'message': 0})


def changedeliverystatus(request):
    if request.session.has_key('RESTAURANTID'):
        id = request.POST.get('order_id')
        splitkey = "--+23+--"
        values = "deliverystatus=out-for-delivery"
        message_1, success = update_table('orderstatus', database, 'id:' + str(id), values, splitkey)
        if success == 1:
            return JsonResponse({'message': 1})
        else:
            return JsonResponse({'message': 0})


def restaurantloginpage(request):
    if not request.session.has_key('RESTAURANTID'):
        return render(request, 'restaurant/restaurantlogin.html')
    else:
        return HttpResponseRedirect('/')

def restaurantloginaction(request):
    if not request.session.has_key('RESTAURANTID'):
        credentials = request.POST.get('signincredentials')
        password = request.POST.get('pwd')

        signupcomplete = False

        if '@' in credentials:
            valid = password_valid(table, database, 'password:' + password, 'email:' + credentials)
            if valid:
                message, rest_info = select(table, database, 'email:' + credentials)
                rest_id = rest_info[0]
                rest_name = rest_info[1]
                rest_email = rest_info[2]
                rest_ownername = rest_info[6]
                rest_address = rest_info[5]
                rest_photo = rest_info[9]

        else:
            valid = password_valid(table, database, 'password:' + password, 'username:' + credentials)
            if valid:
                message, rest_info = select(table, database, 'restaurantname:' + credentials)
                rest_id = rest_info[0]
                rest_name = rest_info[1]
                rest_email = rest_info[2]
                rest_ownername = rest_info[6]
                rest_address = rest_info[5]
                rest_photo = rest_info[9]

        if valid:
            request.session['RESTAURANTID'] = rest_id
            request.session['RESTAURANTNAME'] = rest_name
            request.session['RESTAURANTEMAIL'] = rest_email
            request.session['RESTAURANTADDRESS'] = rest_address
            request.session['RESTAURANTOWNERNAME'] = rest_ownername
            if rest_photo:
                request.session['RESTAURANTPHOTO'] = rest_photo
            return HttpResponseRedirect('/')
        else:
            return JsonResponse({'message': 'Restaurant does not exist'})

    else:
        return HttpResponseRedirect('/')

def restaurantlogout(request):
    try:
        if request.session.has_key('RESTAURANTID'):
            del request.session['RESTAURANTID']
            del request.session['RESTAURANTNAME']
            del request.session['RESTAURANTEMAIL']
            del request.session['RESTAURANTADDRESS']
            del request.session['RESTAURANTOWNERNAME']
            if request.session.has_key('RESTAURANTPHOTO'):
                del request.session['RESTAURANTPHOTO']
            response = {'message': 1}
    except:
        response = {'message': 0}

    return JsonResponse(response)

def restaurantsettingspage(request):

    if request.session.has_key('RESTAURANTID'):
        user_id = request.session['RESTAURANTID']
        message, rest_data = select(table, database, 'id:' + str(user_id))
        rest_list = list(rest_data)

        rest_list.pop(3)
        rest_list.pop(7)

        message_1, city_info = select('city', database, 'id:'+str(rest_list[6]))
        city_name = city_info[1]
        rest_list[6] = city_name
        keys = ['id', 'restaurantname', 'email', 'mobileno', 'address', 'ownername', 'city', 'photo']

        if rest_list:
            rest_dict = make_dictionary(rest_list, keys)
        return render(request, 'restaurant/restaurantsettings.html', {'restaurant': rest_dict})

def restaurantsettingsaction(request):

    if request.session.has_key('RESTAURANTID'):
        id = request.session['RESTAURANTID']
        restaurantname = request.POST.get('restaurantname')
        mobileno = str(request.POST.get('mobileno'))
        address = request.POST.get('address')
        splitkey = '++--+123+--++'

        if restaurantname and mobileno and address:

            request.session['RESTAURANTNAME'] = restaurantname
            valstr = 'restaurantname=' + restaurantname + splitkey + 'mobileno=' + mobileno  \
                      + splitkey + 'address=' + address

            message = update_table(table, database, 'id:'+str(id), valstr, splitkey)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('restaurantsettingspage')
    else:
        return HttpResponseRedirect('/')


def restaurantchangephoto(request):
    if request.session.has_key('RESTAURANTID'):
        id = request.session['RESTAURANTID']
        email = request.session['RESTAURANTEMAIL']
        try:
            photo = request.FILES['photo']
        except:
            photo = None

        splitkey = '++--+123+--++'
        if photo:
            photolocation = image_upload_path + email
            photolocation = write_image(photo, photolocation)
            photolocation = photolocation[7:]
            try:
                message = update_table(table, database, 'id:'+str(id), 'photo='+photolocation, splitkey)
                request.session['RESTAURANTPHOTO'] = photolocation
            except:
                ''
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def restaurantchangepasswordpage(request):
    if request.session.has_key('RESTAURANTID'):
        return render(request, 'restaurant/restaurantchangepassword.html')
    else:
        return HttpResponseRedirect('/')

def restaurantchangepasswordaction(request):
    if request.session.has_key('RESTAURANTID'):
        rest_id = request.session['RESTAURANTID']

        oldpassword = request.POST.get('oldpassword')
        password = request.POST.get('password')

        pass_valid = password_valid(table, database, 'password:'+oldpassword, 'id:'+str(rest_id))
        if pass_valid:
            update_table(table, database, 'id:' + str(rest_id), 'password=' + password, '--++--')
            return JsonResponse({'message': 1})
        else:
            return JsonResponse({'message': 0})
    else:
        return HttpResponseRedirect('/')


def restaurantshowreviews(request):
    if request.session.has_key('RESTAURANTID'):
        rest_id = request.session['RESTAURANTID']
        message_2, reviews = selectfromcolumn('restaurantreview', database, 'restaurantid:'+str(rest_id))
        rest_rating = 0

        for review in reviews:
            rest_rating = (rest_rating + review[3])/2

        final_reviews_list = list()
        message_1, users_tuples = selectall('user', database)
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

        return render(request, 'restaurant/restaurantreview.html', {'all_reviews': review_users_dict, 'rating':
            rest_rating})
    else:
        return HttpResponseRedirect('/')

def checkorders(request):

    if request.session.has_key('RESTAURANTID'):
        rest_id = str(request.session['RESTAURANTID'])

        message, orders_tuples = selectfromcolumn('ordertable', database, 'restaurantid:'+rest_id)
        dates_len = len(orders_tuples)

        order_ids_str = request.POST.get('order_ids')
        order_ids = order_ids_str.split(',')
        length = len(order_ids)

        ids = list()
        for i in order_ids:
            ids.append(int(i))
        new_orders = list()
        new_ids = []
        all_ids = []
        new_orders_ids = list()
        for order in orders_tuples:
            all_ids.append(order[0])

        if dates_len > length:
            for i in all_ids:
                if i not in ids:
                    new_orders_ids.append(i)

            for i in new_orders_ids:
                for order in orders_tuples:
                    if i == order[0]:
                        new_orders.append(order)
                        break
            message = 1
        else:
            message = 0
        #return JsonResponse({'message': str(dates_len) + " , " + str(length)})
        return JsonResponse({'message': message, 'new_orders': new_orders, 'all_ids': all_ids})
    return HttpResponseRedirect('/')

image_upload_path = 'static/uploads/restaurants/'

def write_image(photo,photopath):
    photoname = str(photo)
    if not os.path.exists(photopath):
        os.mkdir(photopath)
    photopath += '/profile'

    if not os.path.exists(photopath):
        os.mkdir(photopath)
    image_path = photopath + "/" + photoname
    with open(image_path, 'wb+') as destination:
        for chunk in photo.chunks():
            destination.write(chunk)

    return image_path

def addrestaurentaction(request):
    restaurantname = request.POST.get('restaurantname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    mobileno = str(request.POST.get('mobileno'))
    address = request.POST.get('address')
    ownername = request.POST.get('ownername')
    city = request.POST.get('city')
    status = request.POST.get('status')

    try:
        photo = request.FILES['photo']
    except:
        photo = None

    splitkey = '++--+123+--++'
    if email and photo:
        photolocation = image_upload_path + email
        photolocation = write_image(photo, photolocation)
        photolocation = photolocation[7:]

    if photo == None:
        photolocation = 'None'

    if restaurantname and email and password and mobileno and address and city and ownername and status:
        message_1, data = select(table, database, 'email:'+email)
        message_2, rest = select(table, database, 'restaurantname:'+restaurantname)
        if not data and not rest:
            splitkey = "-+-+5123+-+"
            message, citydata = select('city', database, 'cityname:'+city)
            cityid = str(citydata[0])
            valstr = restaurantname + splitkey + email + splitkey \
                     + password + splitkey + mobileno + splitkey + address \
                     + splitkey + ownername + splitkey + cityid + splitkey + status + splitkey + photolocation
            message = insert_into_table(table, database, valstr, splitkey)
            return HttpResponseRedirect('/viewrestaurant#'+restaurantname)
        else:
            if data:
                if rest:
                    return HttpResponse('Same Email or Restaurant Name Found')
                else:
                    return HttpResponse('Same Email Found')
            else:
                return HttpResponse('Same Restaurant Name Found')

    return HttpResponse('All Data is mandatory')

def deleterestaurentaction(request):
    restaurantid = request.POST.get('id')
    message, restaurant = select(table, database, 'id:'+restaurantid)

    email = restaurant[2]
    basic_delpath = 'static/uploads/restaurants/'
    delpath_1 = basic_delpath + email
    delpath_2 = basic_delpath + "fooditems/" + restaurantid

    if os.path.exists(delpath_1):
        shutil.rmtree(delpath_1)

    if os.path.exists(delpath_2):
        shutil.rmtree(delpath_2)

    message = delete(table, database, 'id:'+restaurantid)

    return HttpResponseRedirect('viewrestaurant')


def updaterestaurentpage(request):

    restaurantid = request.POST.get('id')
    message, restaurantdata = select(table, database, 'id:'+restaurantid)
    keys = ['id', 'restaurantname', 'email', 'password', 'mobileno', 'address','ownername','city','status','photo']
    #return HttpResponse(restaurantdata)
    if(restaurantdata):
        restaurantcity = value_info('city', database, 'cityname', 'id:' + str(restaurantdata[7]))
        allcities = colum_data('city', database, 'cityname')

        if restaurantcity and allcities:
            restdata = [a for a in restaurantdata]
            cityinfo = {}
            cityinfo['id'] = restdata[7]
            cityinfo['cityname'] = restaurantcity[0]

            restdata[7] = restaurantcity[0]
            senddata = make_dictionary(restdata,keys)
            cities = lists_to_list(allcities)

            if senddata and cities:
                return render(request, 'restaurant/updaterestaurant.html',
             {'data': senddata,'cities': cities, 'cityinfo': cityinfo})

    return HttpResponseRedirect('viewrestaurant')

def updaterestaurentaction(request):
    restaurantid = request.POST.get('id')
    restaurentname = request.POST.get('restaurantname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    mobileno = str(request.POST.get('mobileno'))
    address = request.POST.get('address')
    ownername = request.POST.get('ownername')
    city = request.POST.get('city')
    status = request.POST.get('status')
    try:
        photo = request.FILES['photo']
    except:
        photo = None

    splitkey = '++--+123+--++'
    if (email and photo):
        photolocation = image_upload_path + email
        photolocation = write_image(photo, photolocation)
        photolocation = photolocation[7:]

    cityiddata = value_info('city', database, 'id', 'cityname:'+city)
    if(cityiddata):
        cityid = str(cityiddata[0])

    if (restaurentname and email and password and mobileno and address and cityid and ownername and status):
        splitkey = "+__52-+d+-31+-__+"
        if photo:
            valstr = 'restaurantname=' + restaurentname + splitkey + \
                     'email=' + email + splitkey + 'password=' + password \
                     + splitkey + 'mobileno=' + mobileno + splitkey + 'address=' + address + splitkey \
                     + 'city=' + cityid + splitkey + 'ownername=' + ownername + splitkey \
                     + 'status=' + status + splitkey + 'photo=' + photolocation
        else:
            valstr = 'restaurantname=' + restaurentname + splitkey + 'email=' + email + splitkey + 'password='\
                     + password + splitkey + 'mobileno=' + mobileno + splitkey + 'address=' + address + splitkey\
                     + 'city=' + cityid + splitkey + 'ownername=' + ownername + splitkey \
                     + 'status=' + status

        message = update_table(table, database, 'id:'+restaurantid, valstr, splitkey)
        return HttpResponseRedirect('viewrestaurant')
    else:
        return HttpResponse('All Data is mandatory')
    return HttpResponseRedirect('viewrestaurant')



def searchrestaurant(request):
    search = request.POST.get('search')
    message, restdata = selectall(table, database)
    result = []
    count = 0
    for row in restdata:
        if search in row[1].lower():
            result.append(restdata[count])
        count += 1

    #return HttpResponse(search.lower())
    return HttpResponse(result)


def restaurantsignuppage(request):
    message, citydata = selectall('city', database)
    if citydata:
        cities = []
        for a in citydata:
            # if city is currently active then send the city name
            if (a[2].lower() == 'active'):
                d = {}
                d['cityid'] = a[0]
                d['cityname'] = a[1]
                d['status'] = a[2]
                cities.append(d)

    return render(request, 'restaurant/restaurantsignup.html', {'city':cities})

def restaurantsignupaction(request):
    restaurantname = request.POST.get('restaurantname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    mobileno = str(request.POST.get('mobileno'))
    address = request.POST.get('address')
    ownername = request.POST.get('ownername')
    city = request.POST.get('city')
    status = request.POST.get('status')

    try:
        photo = request.FILES['photo']
    except:
        photo = None

    splitkey = '++--+123+--++'
    if email and photo:
        photolocation = image_upload_path + email
        photolocation = write_image(photo, photolocation)
        photolocation = photolocation[7:]

    if photo == None:
        photolocation = 'None'
    #return HttpResponse(str(restaurantname)+str(email)+str(password)+str(mobileno)+str(address)+str(city)+str(status))
    if restaurantname and email and password and mobileno and address and city and ownername and status:
        message_1, data = select(table, database, 'email:' + email)
        message_2, rest = select(table, database, 'restaurantname:'+restaurantname)

        if not data and not rest:
            splitkey = "-+-+5123+-+"
            message, citydata = select('city', database, 'cityname:' + city)
            cityid = str(citydata[0])

            valstr = restaurantname + splitkey + email + splitkey + password + splitkey + mobileno + splitkey + address\
                      + splitkey + ownername + splitkey + cityid + splitkey + status + splitkey + photolocation

            message = insert_into_table(table, database, valstr, splitkey)
            return JsonResponse({'valid': 1, 'message': 'Your Restaurant Was Added Successfully.Just wait for the approval of the admin'})
        else:
            if data:
                if rest:
                    return JsonResponse({'valid': 0, 'message': ' Same Email or Restaurant Name Found'})
                else:
                    return JsonResponse({'valid': 0, 'message': 'Same Email Found'})
            else:
                return JsonResponse({'valid': 0, 'message': 'Same Restaurant Name Found'})
    v = str(restaurantname) + str(email) + str(password) + str(mobileno) + str(address) + str(city) + str(status)
    return JsonResponse({'valid': 0, 'message': 'Restaurant Info was Invalid'+v})

def addrestaurantreview(request):
    splitkey = "-+-+5123+-+"
    if request.session.has_key('USERID'):
        user_id = request.session['USERID']
        user_email = request.session['USEREMAIL']

        message_1, user_data = select('user', database, 'id:'+str(user_id))
        if user_data:
            review = request.POST.get('review')
            rating = request.POST.get('rating')
            restaurant_id = request.POST.get('restaurant_id')
            date_of_review = datetime.datetime.now()

            if rating and review:
                columns_dict = {'restaurantid': restaurant_id, 'userid': user_id}
                message_2, review_tuple = select_from_columns('restaurantreview', database, columns_dict)

                if not review_tuple:

                    values = restaurant_id + splitkey + review + splitkey + rating + splitkey + str(date_of_review) + \
                             splitkey + str(user_id) + splitkey + user_email + splitkey + 'Active'

                    message_3 = insert_into_table('restaurantreview', database, values, splitkey)
                    return JsonResponse({'message': 'Review Added'})
                else:
                    values = "comment=" + review + splitkey + "rating=" + rating + splitkey +\
                              "dateofreview=" + str(date_of_review)
                    message_4 = update_table('restaurantreview', database, 'id:'+str(review_tuple[0]), values, splitkey)
                    return JsonResponse({'message': message_4})

            else:
                if not rating and not review:
                    d = {'message': 'Rating and Review Both are necessary'}
                elif not rating:
                    d = {'message': 'Rating is necessary'}
                elif not review:
                    d = {'message': 'Review is necessary'}
            return JsonResponse(d)

        else:
            return JsonResponse({'message': 'No User of Id'+user_id})
