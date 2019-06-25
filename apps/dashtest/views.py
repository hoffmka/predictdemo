from django.shortcuts import render

# Create your views here.

def dashtest(request):
    return render(request, 'dash/dashtest.html')