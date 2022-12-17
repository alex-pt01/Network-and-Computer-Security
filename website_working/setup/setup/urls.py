from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from SAH import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', views.home, name='home'),    
    path('account/', views.account, name='account'), 
       
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('signup/', views.signup, name='signup'),
    path('paciente_or_doctor/', views.paciente_or_doctor, name='paciente_or_doctor'),
    path('doctor-signup/', views.doctor_signup, name='doctor-signup'),
    path('pacient-signup/', views.pacient_signup, name='pacient-signup'),

    path('delete-user/<str:id>', views.delete_user, name='delete-user'),
    path('update-user/', views.update_user, name='update-user'),
    path('update-doctor/<str:doctor_id>/', views.update_doctor, name='update-doctor'),
    path('update-pacient/<str:pacient_id>/', views.update_pacient, name='update-pacient'),

    path('consults/', views.consults, name='consults'),
    path('consult-reservation/', views.consult_reservation, name='consult-reservation'),


    #HOSPITAL
    path('consults-management/', views.consults_management, name='consults-management'),
    path('create-consult/', views.create_consult, name='create-consult'),
    path('deleteConsult/<str:id>', views.deleteConsult, name='deleteConsult'),
    path('update-consult/<str:id>/', views.update_consult, name='update-consult'),

    path('rooms-management/', views.rooms_management, name='rooms-management'),
    path('deleteRoom/<str:id>', views.deleteRoom, name='deleteRoom'),
    path('update-room/<str:id>/', views.update_room, name='update-room'),
    path('create-room/', views.create_room, name='create-room'),

    path('users-management/', views.users_management, name='users-management'),
    path('deletePacient/<str:id>', views.deletePacient, name='deletePacient'),
    path('deleteDoctor/<str:id>', views.deleteDoctor, name='deleteDoctor'),

    path('room-consult-management/', views.room_consult_management, name='room-consult-management'),
    path('create-room-consult/', views.create_room_consult, name='create-room-consult'),
    path('deleteRoomConsult/<str:id>', views.deleteRoomConsult, name='deleteRoomConsult'),
    path('update-room-consult/<str:id>/', views.update_room_consult, name='update-room-consult'),

    path('doctor-info/<str:id>/', views.doctor_info, name='doctor-info'),
    path('pacient-info/<str:id>/', views.pacient_info, name='pacient-info'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)