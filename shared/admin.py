from django.contrib import admin
from .models import *

# Register your models here.

_admin = admin.site
_admin.register(MeasumentsUnits)
