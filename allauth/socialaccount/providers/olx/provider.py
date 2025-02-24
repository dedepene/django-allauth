from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.models import SocialAccount, SocialLogin, SocialToken
from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.olx.views import OLXOAuth2Adapter


class OLXProvider(OAuth2Provider):
    id = 'olx'
    name = 'OLX'
    account_class = SocialAccount
    oauth2_adapter_class = OLXOAuth2Adapter

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        return dict(
            email=data.get('email'),
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )

    def extract_email_addresses(self, data):
        ret = []
        email = data.get('email')
        if email:
            ret.append(EmailAddress(email=email, verified=True, primary=True))
        return ret


provider_classes = [OLXProvider]
