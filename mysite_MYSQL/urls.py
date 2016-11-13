"""mysite_MYSQL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


""" redirect http://localhost:8000/ oder zsiv.pythonanywhere.com/""" 
class RootRedirectView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):
        self.url = '/ZSIV/'
        return super(RootRedirectView, self).get_redirect_url(*args, **kwargs)
        




urlpatterns = [
    url(r'^$', RootRedirectView.as_view()),
    #url(r'^$', redirect_to, {'ZSIV': ''}),
    
    url(r'^ZSIV/', include('ZSIV.urls')),
    url(r'^admin/', admin.site.urls),
    # django-registration-redux old
    #url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
]

# aus try django 1.9 , fuer fileupload locations

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    