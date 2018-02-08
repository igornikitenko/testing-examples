from django import test
from django.urls import reverse, NoReverseMatch
from webapp.urls import urlpatterns

skip_urls = (r'/list_params/', r'/post_short',
             r'/admin/', r'/account/', r'/logout', r'/plans',
             r'/password', r'/reset', r'/signup/', r'/activate')


class UrlsTest(test.TestCase):

    def test_responses(self):
        for url in urlpatterns:
            try:
                full_url = reverse(url.name)
                if full_url.startswith(skip_urls):
                    continue
                response = self.client.get(full_url)
            except NoReverseMatch:
                continue
            except AttributeError:
                continue

            print (full_url)
            self.assertEqual(response.status_code, 200)


#---------------------------------------------------------


import unittest
import urllib
from bs4 import BeautifulSoup
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib import auth
from django.conf import settings
from ..models import UserProfile
from ..views import account_settings_view

test_account = settings.TEST_ACCOUNT_NAME
test_pwd = settings.TEST_ACCOUNT_PASSWORD
skip = unittest.skip('')


class CommonSetup(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.user = UserProfile.objects.get(email=test_account)
        self.client = Client()
        self.client.login(email=test_account, password=test_pwd)
        self.factory = RequestFactory()


class UserprofileTest(CommonSetup):
    def test_account_settings(self):
        request = self.factory.get(reverse('account_settings'))
        request.user = self.user
        response = account_settings_view(request)
        self.assertEqual(response.status_code, 200)

    def test_account_api(self):
        response = self.client.get('/account/api/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['key'] is not None)

    def test_login(self):
        self.client.logout()
        user = auth.get_user(self.client)
        assert not user.is_authenticated()
        self.client.post('/login/', dict(username=test_account,
                                         password=test_pwd))
        user = auth.get_user(self.client)
        assert user.is_authenticated()


class LandingTest(CommonSetup):
    def test_landing(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class TrendsTest(CommonSetup):
    def test_trend(self):
        response = self.client.get('/trends/Spain/')
        self.assertEqual(response.status_code, 200)


class DatasetTest(CommonSetup):
    def test_dataset(self):
        response = self.client.get('/dataset/EI_BSCO_M/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'series/dataset.html')


class SourceTest(CommonSetup):
    def test_source(self):
        response = self.client.get('/source/WB/World-Bank/')
        self.assertEqual(response.status_code, 200)


class SearchTest(CommonSetup):
    def test_search_results(self):
        '''
        test that search strings contain results
        test that if page delivers results, previous page was full
        '''
        for search_str in ['gross domestic product spain',
                           'inflation bolivia',
                           'united nations mortality',
                           'ecb']:
            last = 0
            for page in range(1,3):
                url_path = '/search/?' + urllib.urlencode({'st':search_str, 'page':page})
                response = self.client.get(url_path)
                bs = BeautifulSoup(response.content,'html.parser')
                rows = bs.find('div', {'id':'results'})\
                         .find_all('div', {'class','row-fluid panel'})
                num_results = len(rows)
                if page == 1:
                    self.assertEqual(num_results > 0, True)
                elif num_results > 0:
                    self.assertEqual(last, 10)
                else:
                    break
                last = num_results