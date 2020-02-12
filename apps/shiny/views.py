from django.shortcuts import render

# for shiny contents
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests

# Create your views here.

def shiny(request):
    return(render(request, 'shiny/shiny.html'))

def shiny_contents(request):
    response = requests.get('http://localhost:8100')
    soup = BeautifulSoup(response.content, 'html.parser')
    return JsonResponse({'html_contents': str(soup)})