from django.shortcuts import render
from .models import *
def search(request):
    return render(request,'opgg/search.html')

def info(request):
    if request.method == "POST":
        name = request.POST['nickname']
        a = Lol.objects.filter(cha_name=name)[0]

    return render(request,'opgg/info.html',{'a':a } )

def all_user(request):
    user = Lol.objects.all().order_by('rank')

    return render(request,'opgg/alluser.html',{'user':user})
# Create your views here.
