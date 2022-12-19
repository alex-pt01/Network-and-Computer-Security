from django.contrib import admin

# Register your models here.
from SAH.models import *


admin.site.register(Consult)
admin.site.register(Room)
admin.site.register(ConsultRoomReservation)
admin.site.register(DoctorProfilee)
