OLX Provider
============

This document describes how to set up and configure the OLX provider for use with django-allauth.

Setup
-----

1. Add the OLX provider to your Django project by including it in your `INSTALLED_APPS`:

    ```python
    INSTALLED_APPS = [
        ...
        'allauth.socialaccount.providers.olx',
        ...
    ]
    ```

2. Configure the OLX provider by adding the following settings to your `settings.py`:

    ```python
    SOCIALACCOUNT_PROVIDERS = {
        'olx': {
            'APP': {
                'client_id': 'your-client-id',
                'secret': 'your-client-secret',
                'key': ''
            }
        }
    }
    ```

3. Add the OLX provider URLs to your project's `urls.py`:

    ```python
    from django.urls import path, include

    urlpatterns = [
        ...
        path('accounts/', include('allauth.urls')),
        ...
    ]
    ```

Usage
-----

Once the OLX provider is set up and configured, users will be able to log in to your Django project using their OLX social account. The login process will redirect users to the OLX authorization page, where they can grant permission for your application to access their OLX account information.

After successful authorization, users will be redirected back to your application, and their OLX account information will be used to create or update their Django user account.

Examples
--------

Here are some examples of how to use the OLX provider in your Django project:

1. Display a login button for the OLX provider in your templates:

    ```html
    <a href="{% provider_login_url 'olx' %}">Log in with OLX</a>
    ```

2. Handle the login callback in your views:

    ```python
    from allauth.socialaccount.providers.olx.views import OLXOAuth2Adapter
    from allauth.socialaccount.models import SocialLogin, SocialToken

    def olx_login_callback(request):
        adapter = OLXOAuth2Adapter()
        token = SocialToken(token=request.GET['code'])
        login = adapter.complete_login(request, None, token)
        return login
    ```

3. Access the user's OLX account information in your views:

    ```python
    from allauth.socialaccount.models import SocialAccount

    def user_profile(request):
        social_account = SocialAccount.objects.get(user=request.user, provider='olx')
        olx_data = social_account.extra_data
        return render(request, 'user_profile.html', {'olx_data': olx_data})
    ```
