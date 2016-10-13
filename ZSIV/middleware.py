'''
Created on Oct 13, 2016
@author: christian

Ab django 1.10 wird in settings.py MIDDLEWARE anstatt MIDDLEWARE_CLASSES benutzt [1]
Die Django Login required middleware die ich benutzen mag[2]
Another Tutorial[3]
Wichtiges Video, dass Middleware anschliessen erklärt [4]
das diagramm ist nur auf älteren Versionen zu sehen wie auf[5]
Mein django-registration-redux-tutorial [6]

[1] https://docs.djangoproject.com/en/1.10/topics/http/middleware/
[2] http://onecreativeblog.com/post/59051248/django-login-required-middleware
[3] https://simpleisbetterthancomplex.com/tutorial/2016/07/18/how-to-create-a-custom-django-middleware.html
[4] https://www.youtube.com/watch?v=3yKuKQ2fuys
[5] https://docs.djangoproject.com/en/1.8/topics/http/middleware/#hooks-and-application-order 
[6] http://www.tangowithdjango.com/book17/chapters/login_redux.html
'''


        
from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).
    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.auth.middleware.AuthenticationMiddleware'. If that doesn't\
 work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."
        print("der regwest:")
        print(request)
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)

