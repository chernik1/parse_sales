from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .parser.parser import run_programm
# Create your views here.


def index(request):
    result = run_programm()
    return render(request, 'main/index.html')