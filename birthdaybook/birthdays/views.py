# from django.http import HttpResponse
#
# from django.contrib.auth import authenticate, login
#
# def index(request):
#     if request.method == 'GET':
#         pass
#     elif request.method == 'POST':
#         do_something_else()
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return HttpResponse("Hello, world. You're at the polls index.")
#     else:
#         return HttpResponse("Login failed")
#from django.utils import timezone
from django.http import  HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.utils import timezone
from django.template import loader
from .models import Book
from django.http import Http404
from django.shortcuts import render
from datetime import date
import datetime
from  django.db import IntegrityError
from calendar import IllegalMonthError
from dateutil import parser


def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # print(str(request))
    template = loader.get_template('books.html')
    template = loader.get_template('schedule/books.html')
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(request, username=username, password=password)
    # if user is not None:
    #     return HttpResponse("Hello, world. You're at the polls index.")
    # print(dir(request.user))

    print("Index is being callled")
    alerts = get_alerts(request.user)
    context = {
        'birthdays_list': request.user.book_set.all(),
        'bdays': alerts
        # "error_msg":error_msg
    }
    print(request.user.book_set.all())
    return HttpResponse(template.render(context, request))

def para_index(request, error_msg=None):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # print(str(request))
    template = loader.get_template('schedule/books.html')
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(request, username=username, password=password)
    # if user is not None:
    #     return HttpResponse("Hello, world. You're at the polls index.")
    # print(dir(request.user))

    print("Index is being callled")
    context = {
        'birthdays_list': request.user.book_set.all(),
        "error_msg":error_msg
    }
    print(request.user.book_set.all())
    return HttpResponse(template.render(context, request))

def detail(request, birthday_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    try:
        birthday = Book.objects.get(pk=birthday_id)
    except Book.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'schedule/update.html', {'birthday': birthday})

def delete(request, birthday_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    try:
        birthday = Book.objects.get(pk=birthday_id)
        birthday.delete()
    except Book.DoesNotExist:
        raise Http404("Question does not exist")
    return redirect(index)

def update(request,birthday_id):
    name = request.POST['name']
    birthday = request.POST['birthday']
    birthday_id = request.POST['id']
    # print(str(request))
    from dateutil import parser

    print(birthday)
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # print(str(request))
    try:
        dt = parser.parse(birthday).date()
        birthday_obj = Book.objects.get(pk=birthday_id)
        birthday_obj.name = name.lower()
        birthday_obj.birthday = dt
        birthday_obj.save()
        # birthday_obj.date =
    except Book.DoesNotExist:
        # raise Http404("Question does not exist")
        print("Does not Exist")
        return para_index(request, "Birthday for {} does not exist".format(str(name)))
    except IntegrityError as e:
        print("Integrity ")
        return para_index(request, error_msg="Person {} is already present".format(str(name)))
    except ValueError as e:
        print("Value Error ")
        return para_index(request, error_msg="Input data is not valid ")
    except IllegalMonthError as e:
        print("Illegal Error ")
        return para_index(request, error_msg="Month in birthday is not valid ")

    except Exception as e:
        print("Final exception")
        print(str(e))
        return para_index(request, error_msg="Server error".format(str(name)))
    return redirect(index)


def delete_everything(request):
    Book.objects.all().delete()
    return redirect(index)

def add(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    if request.method == 'GET':
            return render(request, 'schedule/add.html', {'date': "Jun 1 2005",'error_msg':None})

    name = request.POST['name']
    birthday = request.POST['birthday']
    if not name or not birthday:
        return render(request, 'schedule/add.html', {'date': "Jun 1 2005", 'error_msg': "Inputs are not valid".format(str(name))})
        # return para_index(request, error_msg="Inputs are not valid".format(str(name)))

    from dateutil import parser

    try:
        dt = parser.parse(birthday).date()
        request.user.book_set.create(name=name.lower(),birthday=dt)

    except IntegrityError as e:
        print("Integrity ")
        return render(request, 'schedule/add.html',
                      {'date': "Jun 1 2005", 'error_msg': "Person {} is already present".format(str(name))})
        # return para_index(request, error_msg="Person {} is already present".format(str(name)))
    except ValueError as e:
        print("Value Error ")
        return render(request, 'schedule/add.html',
                      {'date': "Jun 1 2005", 'error_msg': "Input data is not valid"})

        # return para_index(request, error_msg="Input data is not valid ")
    except IllegalMonthError as e:
        print("Illegal Error ")
        return render(request, 'schedule/add.html',
                      {'date': "Jun 1 2005", 'error_msg': "Month in birthday is not valid"})

        # return para_index(request, error_msg="Month in birthday is not valid ")

    except Exception as e:
        print(str(e))
        return render(request, 'schedule/add.html',
                      {'date': "Jun 1 2005", 'error_msg': "Internal server error"})

        # return para_index(request,error_msg= "Server error".format(str(name)))
    return redirect(index)


def get_alerts(user):
    # if not request.user.is_authenticated:
    #     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # if request.method == 'GET':
    #     return render(request, 'add.html', {'date': "Jun 1 2005"})
    #
    # birthday = request.POST['birthday']
    # name = request.POST['name']

    dt = datetime.datetime.today()
    day = dt.day
    month = dt.month
    # self.
    # dt = None
    blist = Book.objects.filter(user=user, birthday__month=month, birthday__day=day)
    return blist
    # if  not birthday and not name:
    #     return para_index(request, error_msg="Inputs are not valid")
    # try:
    #     if  birthday:
    #         dt = parser.parse(birthday).date()
    #     if not name:
    #         pass
    #     elif not dt:
    #         blist = Book.objects.filter(user=request.user, name=name)
    #     else:
    #         blist = Book.objects.filter(user=request.user, name=name, birthday=dt)
    #     print(blist)
    #     print(type(blist))
    # except IntegrityError as e:
    #     print("Integrity ")
    #     return para_index(request, error_msg="Person {} is already present".format(str(name)))
    # except ValueError as e:
    #     print("Value Error ")
    #     return para_index(request, error_msg="Input data is not valid ")
    # except IllegalMonthError as e:
    #     print("Illegal Error ")
    #     return para_index(request, error_msg="Month in birthday is not valid ")
    #
    # except Exception as e:
    #     print(str(e))
    #     return para_index(request,error_msg= "Server error".format(str(name)))

    # template = loader.get_template('search_results.html')
    # context = {
    #     'birthdays_list': blist,
    # }
    # # print(request.user.book_set.all())
    # return HttpResponse(template.render(context, request))


def search(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.method == 'GET':
        return render(request, 'schedule/search.html', {'date': "Jun 1 2005", 'error_msg': None})

    birthday = request.POST['birthday']
    name = request.POST['name']
    dt = None
    if  not birthday and not name:
        return render(request, 'schedule/search.html', {'date': "Jun 1 2005", 'error_msg': "Invalid inputs"})
        # return para_index(request, error_msg="Inputs are not valid")
    print(name)
    print(birthday)
    name = name.lower()
    print(Book.objects.filter(user=request.user))
    try:
        if  birthday:
            dt = parser.parse(birthday).date()
        if not name:
            blist = Book.objects.filter(user=request.user, birthday=dt)
        elif not dt:
            print("Fetching via name {}".format(name))
            blist = Book.objects.filter(user=request.user, name=name)
        else:
            blist = Book.objects.filter(user=request.user, name=name, birthday=dt)
        print(blist)
        # print(type(blist))
    except IntegrityError as e:
        # print("Integrity ")
        return render(request, 'schedule/search.html', {'date': "Jun 1 2005", 'error_msg': "Person {} is already present".format(str(name))})
    except ValueError as e:
        print("Value Error ")
        return render(request, 'schedule/search.html', {'date': "Jun 1 2005", 'error_msg': "input data is not valid"})
        # return para_index(request, error_msg="Input data is not valid ")
    except IllegalMonthError as e:
        print("Illegal Error ")
        return render(request, 'schedule/search.html', {'date': "Jun 1 2005", 'error_msg': "Month in birthday is not valid"})

    except Exception as e:
        print(str(e))
        return para_index(request,error_msg= "Server error".format(str(name)))

    template = loader.get_template('schedule/search-results.html')
    context = {
        'birthdays_list': blist,
    }
    # print(request.user.book_set.all())
    return HttpResponse(template.render(context, request))


