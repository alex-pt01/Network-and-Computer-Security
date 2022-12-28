from django.contrib import admin

# Register your models here.
from SAH.models import *


admin.site.register(Consult)
admin.site.register(ConsultRoomReservation)
admin.site.register(DoctorProfilee)
admin.site.register(ExternalLabs)
admin.site.register(ExternalLabProfilee)


