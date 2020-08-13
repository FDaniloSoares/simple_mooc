from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View

# Create your views here.
def home(request):
    #return HttpResponse('Vai dar certo, Danilo')
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

from django.views import View

@csrf_exempt
def webhook(request):
    return HttpResponse('pong')
