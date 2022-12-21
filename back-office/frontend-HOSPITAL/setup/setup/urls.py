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
    path('', views.home, name='home'),    
    
    #API
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('doctor-consults/', views.doctor_consults, name='doctor-consults'),

    path('consults-management/', views.consults_management, name='consults-management'),
    path('deleteConsult/<str:id>', views.deleteConsult, name='deleteConsult'),
    path('update-consult/<str:id>/', views.update_consult, name='update-consult'),
    path('create-consult/', views.create_consult, name='create-consult'),

    path('rooms-management/', views.rooms_management, name='rooms-management'),
    path('deleteRoom/<str:id>', views.deleteRoom, name='deleteRoom'),
    path('create-room/', views.create_room, name='create-room'),

    path('external-labs-info/', views.external_labs_info, name='external-labs-info'),
    path('deleteExternalLab/<str:id>', views.deleteExternalLab, name='deleteExternalLab'),
    path('external-labs-info-doctor/', views.external_labs_by_doctor_id_card, name='external-labs-info-doctor'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)