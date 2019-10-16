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
#
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    print(str(request))
    # username = request.POST['username']
    # password = request.POST['password']
    # user = authenticate(request, username=username, password=password)
    # if user is not None:
    #     return HttpResponse("Hello, world. You're at the polls index.")
    print(dir(request.user))
    return HttpResponse(" NOT AUTH Hello, world. You're at the polls index.")