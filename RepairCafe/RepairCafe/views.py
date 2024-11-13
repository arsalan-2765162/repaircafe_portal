from django.shortcuts import render

def index(request):
    return render(request, 'RepairCafe/index.html', context={})
