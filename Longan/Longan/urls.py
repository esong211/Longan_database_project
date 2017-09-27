"""Longan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from LonganApp import views

urlpatterns = [
#To use just normal view, we have to use views.___ and replace the ___ with a function name we want to use in views.py
#In this case, I'm using index function in views.py. So, I replaced it like views.index
    url(r'^$', views.index, name='index'),
    url(r'^careerfair.html/$', views.careerfair, name='careerfair'),
    url(r'^company.html/$', views.company, name='company'),
    url(r'^map.html/', views.maps, name='maps'),
    url(r'^favorites.html/$', views.favorites, name='favorites'),
    url(r'^settings.html/$', views.settings, name='settings'),
    url(r'^login.html/$', views.login_view, name='login_view'),
    url(r'^admin/', admin.site.urls),
    url(r'^addIndustryToPreferences', views.addIndustryToPreferences, name='addIndustryToPreferences'),
    url(r'^removeFromPreferences', views.removeFromPreferences, name='removeFromPreferences'),
    url(r'^addCompanyToFavorites', views.addCompanyToFavorites, name='addCompanyToFavorites'),
    url(r'^unfavoriteCompany', views.unfavoriteCompany, name='unfavoriteCompany'),
    url(r'^loginRequest', views.loginRequest, name='loginRequest'),
    url(r'^logoutRequest', views.logoutRequest, name='logoutRequest'),
    url(r'^signupRequest', views.signupRequest, name='signupRequest'),
    url(r'^deleteCompany', views.deleteCompany, name='deleteCompany'),
    url(r'^deleteCareerfair', views.deleteCareerfair, name='deleteCareerfair'),
    url(r'^addCompany', views.addCompany, name='addCompany'),
    url(r'^addCareerfair', views.addCareerfair, name='addCareerfair'),
    url(r'^updateCompany', views.updateCompany, name='updateCompany'),
    url(r'^updateCareerfair', views.updateCareerfair, name='updateCareerfair'),
    url(r'^filterByCompany', views.filterByCompany, name='filterByCompany'),
    url(r'^filterByCareerfair', views.filterByCareerfair, name='filterByCareerfair')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
