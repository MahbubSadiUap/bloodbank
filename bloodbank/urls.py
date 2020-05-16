"""bloodbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blood_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('register/', views.registerView, name='register'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('profile/', views.profileView, name='profile'),
    path('profile/changepassword/', views.changePasswordView, name='changepassword'),
    path('profile/update/', views.editProfileView, name='updateprofile'),
    path('profile/status/', views.statusView, name='status'),
    path('request/', views.createReqView, name="createreq"),
    path('editrequest/<int:pin>/', views.editRequestView, name="editrequest"),
    path('deleterequest/<int:pin>/', views.deleteRequestView, name="deleterequest"),
    path('getrequest/', views.getRequestView, name="getrequest"),
    path('allrequest', views.allReqView, name='allrequest'),
    path('group/<int:id>/', views.groupView, name='group'),
    path('donor/<int:id>/', views.detailView, name="details"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
