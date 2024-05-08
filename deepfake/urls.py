from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.signup, name='register'),
    path("login",views.login,name='login'),
    path('home',views.home ,name='home'),
    path('contact',views.contact),
    path('about',views.about),
    path('uploadfile', views.upload_file, name='uploadfile'),
    path('result', views.upload_file, name='result'),
  
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)