from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
class Test(View):
    def get(self, request):

        return HttpResponse(content="TEST")