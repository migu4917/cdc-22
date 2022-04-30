from django.contrib import auth
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

# refs:
# https://zhuanlan.zhihu.com/p/378849347
# https://www.runoob.com/django/django-auth.html


@api_view(["POST"])
def login(request):
    if request.method == 'POST':
        data = request.data
        username = data['username']
        password = data['password']
        user = auth.authenticate(username=username, password=password)
        print("username %s, pwd %s" % (username, password))
        if user is not None:
            auth.login(request, user)
            return HttpResponse("succeed", status=status.HTTP_200_OK)
        else:
            print("Wrong Username or password!")
            return HttpResponse("Wrong Username or Password!", status=status.HTTP_401_UNAUTHORIZED)
