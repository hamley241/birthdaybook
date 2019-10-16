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

def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # print(str(request))
    template = loader.get_template('books.html')
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(request, username=username, password=password)
    # if user is not None:
    #     return HttpResponse("Hello, world. You're at the polls index.")
    # print(dir(request.user))

    print("Index is being callled")
    context = {
        'birthdays_list': request.user.book_set.all(),
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
    return render(request, 'detail.html', {'birthday': birthday})

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
    dt = parser.parse(birthday).date()
    print(birthday)
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # print(str(request))
    try:
        birthday_obj = Book.objects.get(pk=birthday_id)
        birthday_obj.name = name
        birthday_obj.birthday = dt
        birthday_obj.save()
        # birthday_obj.date =
    except Book.DoesNotExist:
        raise Http404("Question does not exist")
    return redirect(index)

def add(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    if request.method == 'GET':
            return render(request, 'add.html', {'date': "Jun 1 2005"})

    name = request.POST['name']
    birthday = request.POST['birthday']
    from dateutil import parser
    dt = parser.parse(birthday).date()

    # print(str(request))
    try:
        request.user.book_set.create(name=name,birthday=dt)

    except Exception as e:
        raise HttpResponse("BAD REQUEST")
    return redirect(index)

# def delete(request):
#     if not request.user.is_authenticated:
#         return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
#     user = request.user
#     delete_id = request.
#     user.book_set.delete()