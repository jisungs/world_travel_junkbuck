
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def travel_log(request):
    # return HttpResponse('hello world')
    return render(request, 'travelog/index.html')