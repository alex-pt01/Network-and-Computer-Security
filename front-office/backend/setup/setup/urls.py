from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from SAH import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', views.home, name='home'),    
       
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
    #API https://www.bezkoder.com/django-rest-api/ 
    path("api/signup/", views.SignUpView.as_view()),
    path("api/login/", views.LoginView.as_view()),

    path('api/hosp-consults-reservation/', views.consults_reservation_to_hospital),
    path('api/hosp-consult-reservation/<int:pk>/', views.consult_reservation_to_hospital)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)