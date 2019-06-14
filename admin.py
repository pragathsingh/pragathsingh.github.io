from django.http import *
from django.shortcuts import render,redirect
from dataqueries import *
from forgetpassword import *
from conversions import *
# from pymysql import *
table = "admin"
database = "foodservice"


#opens up AdminSignin Page
def adminsigninpage(request):
    if request.session.has_key('ADMINID'):
        return render(request, 'admin/adminhomepage.html')
    else:
        return render(request, 'admin/admingsignin.html')

def adminsigninaction(request):

    credentials = request.POST.get('signincredentials')
    password = request.POST.get('pwd')

    if not credentials or not password:
        if not credentials and not password:
            return JsonResponse({'valid': 0, 'message': 'email and password are essential'})
        if not credentials:
            return JsonResponse({'valid': 0, 'error_email': 'email is essential'})
        else:
            return JsonResponse({'valid': 0, 'error_pwd': 'password is essential'})

    valid = 0
    if '@' in credentials:
        valid = password_valid(table, database, 'password:' + password, 'emailid:' + credentials)
        if valid:
            message, admin_info = select(table, database, 'emailid:' + credentials)
            admin_id = admin_info[0]
            admin_name = admin_info[1]
            admin_email = admin_info[2]
            admin_photo = admin_info[6]
            admin_type = admin_info[4]

    if valid:
        request.session['ADMINEMAIL'] = admin_email
        request.session['ADMINID'] = admin_id
        request.session['ADMINNAME'] = admin_name
        request.session['ADMINTYPE'] = admin_type
        if admin_photo:
            request.session['USERPHOTO'] = admin_photo
        return JsonResponse({'valid': 1})
    else:
        return JsonResponse({'valid': 0, 'message': 'No Admin with same email'})

def adminlogoutaction(request):

    try:
        del request.session['ADMINID']
        del request.session['ADMINEMAIL']
        del request.session['ADMINNAME']
        del request.session['ADMINTYPE']
        response = {'message': 1}
    except:
        response = {'message': 0}

    return JsonResponse(response)


def adminhomepage(request):
    if request.session.has_key('ADMINID'):
        admin_id = str(request.session['ADMINID'])
        message, rest_not_approved = selectfromcolumn('restaurant', database, 'status:'+"Not Approved")
        if rest_not_approved:
            request.session['RESTAURANTSPENDING'] = len(rest_not_approved)
        else:
            request.session['RESTAURANTSPENDING'] = 0

        return render(request, 'admin/adminhomepage.html')
    else:
        return HttpResponseRedirect('/')

def adminforgetpasswordpage(request):
    return render(request, 'admin/adminforgetpassword.html')

def adminaddpage(request):
    if request.session.has_key('ADMINID'):
        return render(request, 'admin/addadmin.html')
    else:
        return HttpResponseRedirect('/')


def adminview(request):
    if request.session.has_key('ADMINID'):
        message, data = selectall(table, database)
        sendlist = []
        if data:
            for tuple in data:
                d = {}
                d['id'] = tuple[0]
                d['username'] = tuple[1]
                d['password'] = tuple[2]
                d['email'] = tuple[3]
                d['admintype'] = tuple[4]
                d['question'] = tuple[5]
                d['answer'] = tuple[6]
                sendlist.append(d)
        return render(request, 'admin/viewadmin.html', {'data': sendlist})
    else:
        return HttpResponseRedirect('/')

def admindelete(request):
    if request.session.has_key('ADMINID'):
        id = request.POST.get('id')
        try:
            message = delete(table, database, 'id:'+id)
            return HttpResponseRedirect('adminview')
        except:
            return HttpResponseRedirect('adminview')

def adminaddaction(request):
    if request.session.has_key('ADMINID'):
        splitkey = "#+-+123-+-#"

        username = request.POST.get('username')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        admintype = request.POST.get('admintype')
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        values = username + splitkey + pwd + splitkey + email + splitkey + admintype + splitkey\
                 + question + splitkey + answer

        user_exist = False
        colstr = 'username,emailid'
        if(username and email and pwd and admintype and question and answer):
            data = credentials_valid(table, database, colstr, [username, email])
            if (data):
                if(data[0] and data[1]):
                    return HttpResponseRedirect('adminaddpage')
                else:
                    try:
                        message = insert_into_table(table,database,values,splitkey)
                        return HttpResponseRedirect('adminview')
                    except:

                        return HttpResponseRedirect('adminaddpage')
        return HttpResponseRedirect('adminaddpage')

def V_D(keystr,values):
    keylist = keystr.split(",")
    if len(keylist) == len(values):
        d = {}
        for a in range(0, len(values)):
            d[keylist[a]] = values[a]
        return d
    return None

def adminupdatepage(request):
    if request.session.has_key('ADMINID'):
        if request.session['ADMINTYPE'] == 'admin':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('pwd')
            admintype = request.POST.get('admintype')
            question = request.POST.get('question')
            answer = request.POST.get('answer')
            values = [username, email, password, admintype, question, answer]
            keystr = "username,email,password,admintype,question,answer"
            data = V_D(keystr, values)
            if data:
                return render(request, 'admin/updateadmin.html', {'data': data})
        else:
            return JsonResponse({'message': 'Sub-admins are not allowed to update admins'})

def adminupdateaction(request):
    if request.session.has_key('ADMINID'):
        splitkey = "++|,|++"            #this key is used to split data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        admintype = request.POST.get('admintype')
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        #username = "'" + username + "'"
        colstr = "username=" + username + splitkey + "emailid=" + email + splitkey + \
                 "password=" + password + splitkey + "admintype=" + admintype + splitkey + \
                 "securityquetion=" + question + splitkey + "answer=" + answer
        if (username and email and password and admintype and question and answer):
            data = update_table(table, database, "username:" +"'"+ username +"'", colstr, splitkey)
            return HttpResponseRedirect('adminview')


def adminforgetpasswordaction(request):
    if not request.session.has_key('ADMINID'):
        admin_email = request.POST.get('email')

        message, admin_info = select(table, database, 'emailid:'+admin_email)
        if admin_info:
            random_link = changeidtolink(str(admin_info[0]))
            send_link = ""
            send_link += " 127.0.0.1:8000/" + 'adminforgetpasswordredirect/' + random_link

            forgetpassword(send_link, admin_email)
            return JsonResponse({'message': 'An email was sent to your email.There is a link which will redirect you to'
                                            'Change password page.'})
    return JsonResponse({'message': 'There is no user with this email'})

def adminforgetpasswordredirect(request,random_link):
    id, date = decodelink(random_link)
    if time.time() - date < 3600:
        message, user_info = select(table, database, 'id:'+id)
        if user_info:
            request.session['ADMINID'] = user_info[0]
            request.session['ADMINEMAIL'] = user_info[3]
            request.session['ADMINNAME'] = user_info[1]
            request.session['ADMINTYPE'] = user_info[4]
            return render(request, 'admin/adminnewpassword.html')
    else:
        return JsonResponse({'message': 'The link has expired'})

def adminchangepassword(request):
    if request.session.has_key('ADMINID'):
        admin_id = request.session['ADMINID']
        password = request.POST.get('password')
        update_table(table, database, 'id:' + str(admin_id), 'password=' + password, '--++--')
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def showsalesdatewise():
    con, cr = connect()
    s = "select dateoforder,sum(amount) from ordertable group by dateoforder"
    cr = con.cursor()
    cr.execute(s)
    result = cr.fetchall()
    con.close()
    r = []
    for p in result:
        d = {}
        d['label'] = p[0]
        d['y'] = p[1]
        r.append(d)
    return r

def adminapproverestaurant(request):
    if request.session.has_key('ADMINID'):
        id = request.POST.get('id')
        if id:
            message_2, success = update_table('restaurant', database, 'id:'+id, 'status=Approved', '++-123-++')
            if success:
                return HttpResponseRedirect('/viewrestaurant')
            else:
                return HttpResponse(message_2)

def adminrevokerestaurantapproval(request):
    if request.session.has_key('ADMINID'):
        id = request.POST.get('id')
        if id:
            message_2, success = update_table('restaurant', database, 'id:'+id, 'status=Not Approved', '++-123-++')
            if success:
                return HttpResponseRedirect('/viewrestaurant')
            else:
                return HttpResponse(message_2)


def viewrestaurentpage(request):

    error = False
    message, restaurantdata = selectall('restaurant', database)
    message, citydata = selectall('city', database)
    restkeys = ['id', 'restaurantname', 'email', 'password', 'mobileno', 'address', 'ownername', 'city', 'status', 'photo']
    citykeys = ['id', 'name', 'status']
    heads = ['Id', 'Restaurant Name', 'Email', 'Password', 'Mobileno', 'Address', 'Ownername', 'City', 'Status', 'Photo']

    if restaurantdata and citydata:

        restlist = tuples_to_dictionaries(restaurantdata,restkeys)
        citydict = tuple_to_onekeydic(citydata)

        if restlist and citydict:

            for index in range(0,len(restlist)):
                rowcityid = restlist[index]['city']

                if rowcityid in citydict:
                    restlist[index]['city'] = citydict[rowcityid]

            return render(request, 'admin/viewrestaurant.html', {
                'data': restlist, 'heads': heads})

    return HttpResponseRedirect('/')

def adminapproverestaurantpage(request):
    error = False
    message, restaurantdata = selectfromcolumn('restaurant', database, 'status:Not Approved')
    message, citydata = selectall('city', database)
    restkeys = ['id', 'restaurantname', 'email', 'password', 'mobileno', 'address', 'ownername', 'city', 'status',
                'photo']
    citykeys = ['id', 'name', 'status']
    heads = ['Id', 'Restaurant Name', 'Email', 'Password', 'Mobileno', 'Address', 'Ownername', 'City', 'Status',
             'Photo']

    if restaurantdata and citydata:

        restlist = tuples_to_dictionaries(restaurantdata, restkeys)
        citydict = tuple_to_onekeydic(citydata)

        if restlist and citydict:

            for index in range(0, len(restlist)):
                rowcityid = restlist[index]['city']

                if rowcityid in citydict:
                    restlist[index]['city'] = citydict[rowcityid]

            return render(request, 'admin/approverestaurant.html', {
                'data': restlist, 'heads': heads})

    return HttpResponseRedirect('/')


def addrestaurentpage(request):
    message, citydata = selectall('city', database)
    if citydata:
        cities = []
        for a in citydata:
            # if city is currently active then send the city name
            if a[2].lower() == 'active':
                d = {}
                d['cityid'] = a[0]
                d['cityname'] = a[1]
                d['status'] = a[2]
                cities.append(d)
        return render(request, 'admin/addrestaurant.html', {'city': cities})

    return HttpResponse('There was a problem Getting the cities')

def adminsettingspage(request):
    if request.session.has_key('ADMINID'):
        admin_id = str(request.session['ADMINID'])

        message, data = select(table, database, 'id:'+admin_id)
        if data:
            d = {}
            d['id'] = data[0]
            d['username'] = data[1]
            d['password'] = data[2]
            d['email'] = data[3]
            d['admintype'] = data[4]
            d['question'] = data[5]
            d['answer'] = data[6]
            return render(request, 'admin/adminsettings.html', {'admin': d})
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def adminsettingsaction(request):
    if request.session.has_key('ADMINID'):
        splitkey = "++|,|++"
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        answer = request.POST.get('answer')
        id = request.POST.get('id')

        colstr = "username=" + username + splitkey + "password=" + password + splitkey + "answer=" + answer
        if username and password and answer:
            data = update_table(table, database, "id:"+str(id), colstr, splitkey)
            return HttpResponseRedirect('/adminsettingspage')
    return HttpResponseRedirect('/')