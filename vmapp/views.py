from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.views.decorators.http import require_POST
from vmapp.vmman import *
from .utils import *
from . import config


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        if request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, "Please logout first!")
            return render(request, 'vmapp/login.html')
        else:
            user = auth.authenticate(username=username, password=password)
            if not user:
                messages.add_message(request, messages.ERROR, "Wrong username or password!")
                return render(request, 'vmapp/login.html')
            else:
                auth.login(request, user)
                return redirect('/')
    else:
        return render(request, 'vmapp/login.html')


@login_required
def index(request):
    vmlist = get_all_vm_list()
    return render(request, 'vmapp/index.html', {"vmlist": vmlist})


@login_required
@require_POST
def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "You have logout.")
    return redirect('login/')
