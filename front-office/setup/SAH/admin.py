from django.contrib import admin

# Register your models here.
from SAH.models import *

admin.site.register(Specialization)
admin.site.register(Doctor)
admin.site.register(Consult)
admin.site.register(Pacient)
