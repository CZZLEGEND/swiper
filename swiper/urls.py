"""swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

from user import apis as user_apis

urlpatterns = [
    url(r'^api/user/get_vcode', user_apis.get_vcode),
    url(r'^api/user/submit_vcode', user_apis.submit_vcode),
    url(r'^api/user/get_profile', user_apis.get_profile),
    url(r'^api/user/set_profile', user_apis.set_profile),
    url(r'^api/user/upload_avatar', user_apis.upload_avatar),
]
