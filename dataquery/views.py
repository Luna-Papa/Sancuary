from django.shortcuts import render


# Create your views here.


def sfcx(request):
    if request.method == 'GET':
        return render(request, 'dataquery/sfcx.html')


def pos(request):
    if request.method == 'GET':
        return render(request, 'dataquery/pos.html')


def account(request):
    if request.method == 'GET':
        return render(request, 'dataquery/account.html')
