from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from SAH import views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
    
    #API
    path("api/signup/", views.SignUpView.as_view()),
    path("api/login/", views.LoginView.as_view()),
    path('api/doct-consults/<str:doctor_id_card>', views.doctor_consults),
    path('api/hosp-consults/', views.hospital_consults),
    path('api/room/', views.room),
    path('api/room_consult/', views.room_consult),
    path('api/external_lab/', views.external_lab),

    #to delete = ao hosp-consults 
    path("api/h-consults/", views.hosp_consults),




    #templates
    path('admin/', admin.site.urls),    
    path('', views.home, name='home'),    
    
    #path('login/', views.login, name='login'),
    #path('signup/', views.signup, name='signup'),
    #path('logout/', views.logout, name='logout'),
    
    #path('consults-management/', views.consults_management, name='consults-management'),
    #path('create-consult/', views.create_consult, name='create-consult'),
    #path('deleteConsult/<str:id>', views.deleteConsult, name='deleteConsult'),
    #path('update-consult/<str:id>/', views.update_consult, name='update-consult'),
    
    #path('rooms-management/', views.rooms_management, name='rooms-management'),
    #path('deleteRoom/<str:id>', views.deleteRoom, name='deleteRoom'),
    #path('update-room/<str:id>/', views.update_room, name='update-room'),
    #path('create-room/', views.create_room, name='create-room'),

    #path('room-consult-management/', views.room_consult_management, name='room-consult-management'),
    #path('create-room-consult/', views.create_room_consult, name='create-room-consult'),
    #path('deleteRoomConsult/<str:id>', views.deleteRoomConsult, name='deleteRoomConsult'),
    #path('update-room-consult/<str:id>/', views.update_room_consult, name='update-room-consult'),

    #path('doctor-info/<str:id>/', views.doctor_info, name='doctor-info'),
    #path('pacient-info/<str:id>/', views.pacient_info, name='pacient-info'),

    #path('external-lab-info/', views.external_lab_info, name='external-lab-info'),
    #path('create-external-lab-info/', views.create_external_lab_info, name='create-external-lab-info'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)