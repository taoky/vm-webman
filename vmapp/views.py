from django.shortcuts import render
from django.contrib import messages, auth


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        if request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, "Please logout first!")
        else:
            user = auth.authenticate(username=username, password=password)
            if not user:
                messages.add_message(request, messages.ERROR, "Wrong username or password!")
            else:
                auth.login(request, user)
        return render(request, 'vmapp/login.html')
