from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import OLXProvider

urlpatterns = default_urlpatterns(OLXProvider)
