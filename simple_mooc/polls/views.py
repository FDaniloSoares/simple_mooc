import hmac
from hashlib import sha1
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_bytes

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
    # Verify the request signature
    header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    if header_signature is None:
        return HttpResponseForbidden('Permission denied.')

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        return HttpResponseServerError('Operation not supported.', status=501)

    mac = hmac.new(force_bytes(settings.GITHUB_WEBHOOK_KEY), msg=force_bytes(request.body), digestmod=sha1)
    if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
        return HttpResponseForbidden('Permission denied.')

    # If request reached this point we are in a good shape
    return HttpResponse('pong')

