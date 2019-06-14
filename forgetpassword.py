import smtplib
from random import *
from string import *
import time


def id_generator(size=6, chars= ascii_letters + digits):
    return ''.join(choice(chars) for _ in range(size))

id_strings = 'AcNgHomPpz'
date_strings_1 = 'dLsgTrwc=v'
date_strings_2 = 'kn,aeCi=Vf'

def changeidtolink(id):
    link = id_generator()
    for a in id:
        index = int(a)
        link += id_strings[index]
    idend = (choice(digits))
    link += idend

    stime = str(time.time())
    date_list = stime.split('.')
    date_part_1 = date_list[0]
    date_part_2 = date_list[1]

    for a in date_part_1:
        index = int(a)
        link += date_strings_1[index]
    link += choice(digits)
    for a in date_part_2:
        index = int(a)
        link += date_strings_2[index]

    link += choice(digits)
    endpart = randrange(30, 50)
    link += id_generator(size=endpart)

    link += choice(digits)
    return link

def decodelink(link):

    main_link = link[6:]
    f_digit = 0
    index = 0
    for a in main_link:
        if a in digits:
            f_digit = index
            break
        index += 1

    id_str = main_link[:f_digit]
    id = ''
    for a in id_str:
        index = id_strings.find(a)
        id += str(index)

    main_link = main_link[f_digit+1:]

    index = 0
    for a in main_link:
        if a in digits:
            f_digit = index
            break
        index += 1

    date_str = main_link[:index]
    main_link = main_link[index+1:]
    date_1 = ''
    for a in date_str:
        index = date_strings_1.find(a)
        date_1 += str(index)

    index = 0
    for a in main_link:
        if a in digits:
            f_digit = index
            break
        index += 1

    date_str = main_link[:index]

    date_2 = ''
    for a in date_str:
        index = date_strings_2.find(a)
        date_2 += str(index)

    date = float(date_1 + "." + date_2)

    return id, date

def forgetpassword(link,receivers):
    sender = 'naruto300696@gmail.com'
    password = 'Pragath1!'
    message = "There was a request for password recovery if it was'nt you then ignore  otherwise\nPlease click on the" \
              " following link to go to password recover page" + link

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receivers, message)
        smtpObj.quit()
    except smtplib.SMTPException:
        print("Error: unable to send email")

