import json
from django.test import TestCase, RequestFactory
from allauth.socialaccount.models import SocialApp, SocialToken
from allauth.socialaccount.providers.olx.provider import OLXProvider
from allauth.socialaccount.providers.olx.views import OLXOAuth2Adapter
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin
from allauth.account.models import EmailAddress

class OLXProviderTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.app = SocialApp.objects.create(
            provider='olx',
            name='OLX',
            client_id='client-id',
            secret='client-secret',
        )
        self.token = SocialToken(token='test-token')

    def test_extract_uid(self):
        provider = OLXProvider()
        data = {'id': '12345'}
        uid = provider.extract_uid(data)
        self.assertEqual(uid, '12345')

    def test_extract_common_fields(self):
        provider = OLXProvider()
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User'
        }
        common_fields = provider.extract_common_fields(data)
        self.assertEqual(common_fields['email'], 'test@example.com')
        self.assertEqual(common_fields['username'], 'testuser')
        self.assertEqual(common_fields['first_name'], 'Test')
        self.assertEqual(common_fields['last_name'], 'User')

    def test_extract_email_addresses(self):
        provider = OLXProvider()
        data = {'email': 'test@example.com'}
        email_addresses = provider.extract_email_addresses(data)
        self.assertEqual(len(email_addresses), 1)
        self.assertEqual(email_addresses[0].email, 'test@example.com')
        self.assertTrue(email_addresses[0].verified)
        self.assertTrue(email_addresses[0].primary)

    def test_complete_login(self):
        adapter = OLXOAuth2Adapter()
        request = self.factory.get('/accounts/olx/login/callback/')
        app = self.app
        token = self.token
        response_data = {
            'id': '12345',
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User'
        }
        with self.settings(SOCIALACCOUNT_PROVIDERS={'olx': {'APP': {'client_id': 'client-id', 'secret': 'client-secret'}}}):
            response = self.client.get('/accounts/olx/login/callback/', data={'code': 'test-code'})
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith('/accounts/profile/'))
            login = SocialLogin(account=adapter.get_provider().sociallogin_from_response(request, response_data))
            complete_social_login(request, login)
            self.assertEqual(login.account.uid, '12345')
            self.assertEqual(login.account.user.email, 'test@example.com')
            self.assertEqual(login.account.user.username, 'testuser')
            self.assertEqual(login.account.user.first_name, 'Test')
            self.assertEqual(login.account.user.last_name, 'User')
            email_address = EmailAddress.objects.get(user=login.account.user)
            self.assertEqual(email_address.email, 'test@example.com')
            self.assertTrue(email_address.verified)
            self.assertTrue(email_address.primary)
