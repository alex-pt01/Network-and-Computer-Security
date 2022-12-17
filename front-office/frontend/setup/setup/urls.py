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



    path('consults/', views.consults, name='consults'),
    path('consult-reservation/', views.consult_reservation, name='consult-reservation'),






]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)