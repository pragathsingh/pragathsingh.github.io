import string

def all_validations(data):

    send = {}

    username = data[0]
    email = data[1]
    password = data[2]
    mobile = data[3]

    username_error = username_check(username)
    email_error = email_check(email)
    password_error = password_check(password)
    mobile_error = mobile_check(mobile)

    send['username'] = username_error
    send['password'] = email_error
    send['email'] = password_error
    send['mobile'] = mobile_error
    return send


def one_validation(key,value):

    send = {}
    if key == 'username':
        if value:
            send['username'] = username_check(value)

    elif key == 'password':
        if value:
            pwd_err_msg = password_check(value)
            send['password'] = pwd_err_msg

    elif key == 'confirmpassword':
        message = 'Password should be same'
        password = value.split(',')[0]
        confirmpassword = value.split(',')[1]
        if password == '':
            message = ''
        if password == confirmpassword:
            message = ''
        send['confirmpassword'] = message

    elif key == 'email':
        if value:
            email_err_msg = email_check(value)
            send['email'] = email_err_msg
        else:
            send['email'] = ''

    elif key == 'mobile':
        if value:
            mob_err_msg = mobile_check(value)
            send['mobile'] = mob_err_msg
        else:
            send['mobile'] = ''

    return send

def password_check(password):
    digits_true = False
    lowecase_true = False
    uppercase_true = False
    punctuations_true = False
    minlength_true = False
    maxlength_true = False
    space_at_ends = False

    min_length = 8
    max_length = 50
    password_length = 0

    ascii_lowercase = list(string.ascii_lowercase)
    ascii_uppercase = list(string.ascii_uppercase)
    digits = list(string.digits)
    punctuations = list(string.punctuation)
    whitespace = list(string.whitespace)
    printable = list(string.printable)
    index = 0

    error_message = ""
    for each in password:
        if (each in digits):
            digits_true = True

        if(each in ascii_lowercase):
            lowecase_true = True

        if(each in ascii_uppercase):
            uppercase_true = True

        if(each in punctuations):
            punctuations_true = True

        if(each in whitespace):
            if(index == 0 and index == len(password)):
                space_at_ends = True

        if (each in printable):
            password_length += 1

    if(password_length < min_length):
        minlength_true = True
    if(password_length > max_length):
        maxlength_true = True

    if(password_length == 0 ):
        error_message = "Enter Password"

    elif(minlength_true):
        if(maxlength_true):
            error_message = "Please use at least 8 characters and maximum 50 characters"
        else:
            error_message = "Please use at least 8 characters for password"

    elif(space_at_ends):
        error_message = "Whitespace should not be at starting and end of passwords"
    else:

        error_message = "Password should contain at least 1 "

        if not digits_true :
            error_message += " number"

        if not uppercase_true :
            if digits_true:
                error_message += " uppercase"
            else:
                error_message += " ,uppercase"

        if not lowecase_true:
            if digits_true and uppercase_true:
                error_message += " lowercase"
            else:
                error_message += " , lowercase"

        if not punctuations_true:
            if digits_true and uppercase_true and lowecase_true:
                error_message += " punctuations"
            else:
                error_message += " and punctuations"

        if digits_true and lowecase_true and uppercase_true and punctuations_true:
            error_message = ""


    return error_message

def email_check(email):

    length = len(email)
    atsign = False
    atsign_count = 0
    domain_empty = False
    domain_dots_at_ends = False

    localparts_successive_dots = False
    localpart_empty = False
    localpart_max_length = 64
    localpart_length = 0
    localpart_dots = False
    lp_max_len_exc = False

    error_message = ""



    if '@' in email:
        atsign = True
        for each in email:
            if each == '@':
                atsign_count += 1

    if atsign_count > 1:
        error_message = "There should be only 1 @ symbol in a email"
        return error_message

    if atsign:
        if '@' == email[0]:
            localpart_empty = True
        if '@' == email[length-1]:
            domain_empty = True

    if not atsign:
        error_message = "email you entered was not valid it should contain @ sign"
        return error_message
    else:
        error_message = "email you entered was not valid "
        if localpart_empty and domain_empty:
            error_message += "  right and left side of '@' should not be empty.At left side domain"
            return error_message
        else:
            if localpart_empty:
                error_message += " right of '@' should not be empty."
            if domain_empty:
                if localpart_empty:
                    error_message += " and domain should not be empty."
                else:
                    error_message += " domain should not be empty."
                return error_message
            if not domain_empty and not localpart_empty:
                error_message = ''

    localpart_length = email.find('@') + 1

    # for each in email:
    #     if :
    #         ''

    #for each in email
    if localpart_length > localpart_max_length:
        lp_max_len_exc = True
    if lp_max_len_exc:
        return 'There Should be 64 or less characters at right side of @'
    #for each in email:

    return error_message

def username_check(username):

    username_len = len(username)
    username__max_len = 15
    username_invalid = False
    ascii_letters = string.ascii_letters
    valid_username_characters = list(string.digits+ascii_letters)

    if username_len == 0:
        return "Username shouldn't be empty"

    if username_len > username__max_len:
        return 'Username should only be of at most 15 characters '

    for each in username:
        if each not in valid_username_characters:
            username_invalid = True
            break

    if username_invalid:
        return 'Username Should Only Contain Alphabets and Digits.'

    return ''

def mobile_check(mobile):

    mobile_max_len = 10
    mobile_len = len(mobile)

    letters_in_mobile = False
    ascii_letters = list(string.ascii_letters)
    for each in mobile:
        if each in ascii_letters:
            letters_in_mobile = True
            break

    if letters_in_mobile:
        return 'There Should not be any characters in a mobile number.'

    if mobile_len < mobile_max_len:
        return 'You entered less digits.There should be 10 digits in a mobile number.'
    if mobile_len > mobile_max_len:
        return 'You entered more than 10 digits.There should be only 10 digits in a mobile number.'
    return ''
