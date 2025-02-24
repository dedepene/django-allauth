from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.socialaccount.providers.olx.provider import OLXProvider
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin, SocialToken
from allauth.account.models import EmailAddress

class OLXOAuth2Adapter(OAuth2Adapter):
    provider_id = OLXProvider.id
    access_token_url = 'https://www.olx.bg/api/open/oauth/token'
    authorize_url = 'https://www.olx.bg/api/open/oauth/authorize'
    profile_url = 'https://www.olx.bg/api/open/v2/users/me'

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': f'Bearer {token.token}'}
        response = requests.get(self.profile_url, headers=headers)
        response.raise_for_status()
        extra_data = response.json()
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        return complete_social_login(request, login)
