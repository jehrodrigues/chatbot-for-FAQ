"""spotify URL Configuration

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
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include, url
from django.contrib import admin
from smartsupport.views import record_list #RecordView, GenreView, BandView, record_detail,

router = routers.DefaultRouter()
#router.register(r'records',RecordView)
#router.register(r'genres',GenreView)
#router.register(r'bands',BandView)

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    #url(r'^records/$', views.RecordView.as_view(), name='record-list'),
    #url(r'', include(router.urls)),
    #url(r'^record/$', record_detail),
    url(r'^record/$', record_list),
    #url(r'^record/(?P<pk>[0-9]+)$', record_detail),
    #url(r'^genres/$', views.GenreView.as_view({'get': 'list'}), name='genre-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
