from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

import requests
from ipaddress import ip_address, ip_network

# Create your views here.
def home(request):
    #return HttpResponse('Vai dar certo, Danilo')
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

@csrf_exempt
def webhook(request):
    #verify if request came from github
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print(forwarded_for)
    if forwarded_for:
        ip = forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    ip_formated = u'{}'.format(ip)
    print(ip_formated)
    client_ip_address = ip_network(ip_formated)
    whitelist = requests.get('https://api.github.com/meta').json()['hooks']

    for valid_ip in whitelist:
        if client_ip_address in ip_network(valid_ip):
            break
        else:
            return HttpResponseForbidden('Permission denied.')
    return HttpResponse('WebHook Works!!!')

