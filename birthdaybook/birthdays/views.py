from django.http import HttpResponse

from django.contrib.auth import authenticate, login

def index(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        do_something_else()
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("Hello, world. You're at the polls index.")
    else:
        return HttpResponse("Login failed")

