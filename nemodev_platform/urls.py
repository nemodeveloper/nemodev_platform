"""nemodev_platform URL Configuration

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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from tastypie.api import Api


from nemodev_platform import settings
from src.apps.quotes.tastypie_api import QuoteResource, CategoryResource, AuthorResource

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index_view'),
    url(r'^quotes/', include('src.apps.quotes.urls', namespace='quotes')),
]

v1_api = Api(api_name='v1')
v1_api.register(QuoteResource())
v1_api.register(CategoryResource())
v1_api.register(AuthorResource())

api_urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
]

urlpatterns += api_urlpatterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

