from django.core.management import call_command
from shutil import copyfile
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vmwebman.settings")

django.setup()  # setup django environment
# Migrate database
call_command("makemigrations", "vmapp")
call_command("migrate")

# Create super user for admin panel
call_command("createsuperuser")

from django.contrib.auth.models import Group

group = Group(name="change_power_operation")
group.save()

copyfile("vmapp/config.sample.ini", "vmapp/config.ini")

print("OK! Now modify vmapp/config.ini, and run `python manage.py runserver` to run server")
