from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .utils import *


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
    return redirect('/login/')


@login_required
def detail(request, section, vm_id, vm_type):
    vm_detail = get_one_vm_detail(vm_id, vm_type, section)
    return render(request, 'vmapp/detail.html', {"vm_detail": vm_detail, "vm_id": vm_id,
                                                 "type": vm_type, "section": section})


@login_required
def state(request, section, vm_id, vm_type):
    if request.method == "GET":
        # show state and chosen form
        vm_now_state = get_one_vm_state(vm_id, vm_type, section)
        return render(request, 'vmapp/state.html', {"vm_now_state": vm_now_state, "vm_id": vm_id,
                                                    "type": vm_type, "section": section,
                                                    "permission": can_change_power_permission(request.user)})
    elif request.method == "POST":
        # handle user request
        if not can_change_power_permission(request.user):
            messages.add_message(request, messages.ERROR, "Permission denied.")
            return redirect('/')
        new_state = request.POST.get("new_state")
        if new_state not in ("on", "off", "pause", "unpause", "shutdown", "suspend"):
            messages.add_message(request, messages.ERROR, "Wrong request.")
            return redirect('/')
        try:
            res = update_one_vm_state(vm_id, vm_type, section, new_state)
            messages.add_message(request, messages.INFO, "Your operation is performed successfully.")
        except ValueError as e:
            messages.add_message(request, messages.ERROR, e)
        return redirect('/')
