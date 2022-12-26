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
   
    path('admin/', admin.site.urls),    
    path("api/signup/", views.SignUpView.as_view()),
    path("api/login/", views.LoginView.as_view()),
    path("api/doctors/", views.doctors),
    path("api/profile/", views.fill_profile),
    path("api/doctor-profile/", views.doctor_profile),
    path("api/check-is-admin/", views.check_is_admin),

    path('api/all-consults/', views.all_doctors),
    
    #Pacient
    path('api/pacient-consults/', views.pacient_consults),

    #Doctor
    path('api/doctor-consults/', views.doctor_consults),
    path("api/create-consult/", views.create_consult),
    path('api/doctor-profile-by-id/', views.doctor_profile_by_id),
    
    #CRUD consults
    path('api/doct-consults/<str:doctor_id_card>', views.doctor_consults),
    path('api/hosp-consult/<str:id>', views.hospital_consult),
    path('api/hospital-consult-by-id/', views.hospital_consult_by_id),

    #CRUD room reservation
    path('api/del-room/<str:id>', views.del_room_reservation),
    path('api/all-room-reservations/', views.all_room_reservations),
    path('api/create-room-reservation/', views.create_room_reservation),

    #External labs
    path('api/external-labs/', views.external_labs_report),
    path('api/create-external-labs/', views.create_external_labs_report),
    path('api/del-external-lab/<str:id>', views.del_lab),
    path('api/external-labs-by-doct_id_card/', views.external_labs_by_doctor_id_card),


    #Protocol
    path('protocol/hello/', views.hello),    
    path('protocol/dh/', views.DH),    
    path("protocol/signup/", views.SignUpView_External_Lab.as_view()),
    path('protocol/profileExternal/', views.fill_profile_external_lab),  
    path('protocol/login/', views.Login_External_View),   



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)