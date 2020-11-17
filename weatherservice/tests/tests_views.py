# To run the test, all you need to do is to run the commands :  python manage.py test weatherservice   (for macOS/Linux )
# in case the test_api_key returns a 401 code, You may need to get a valid api key from the api source here https://home.openweathermap.org/

from django.test import TestCase, Client
from django.urls import reverse
import json
from django.conf import settings
from django.contrib.auth.models import User
import requests



class TestViews(TestCase):
    def setUp(self):
        self.city = 'london'
        self.appid = 'test api key'

        self.user = User.objects.create_user(
            username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')

    def test_api_key(self):
        response = requests.get('http://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}'.format(city = self.city, appid=settings.API_KEY))
        self.assertEquals(response.status_code, 200)
    
    def test_home_view(self):
        response = self.client.get(reverse('weatherservice:home', args=[self.city]))
        self.assertEquals(response.status_code, 200)

    def test_temp_conf_view(self):
        response = self.client.get(reverse('weatherservice:temp_unit', args=[self.city, 'celsius']))
        self.assertEquals(response.status_code, 200)

    def test_wrong_temp_conf_view(self):
        response = self.client.get(reverse('weatherservice:temp_unit', args=[self.city, 'c']))
        self.assertEquals(response.status_code, 404)

    def test_wrong_input(self):
        response = self.client.get(reverse('weatherservice:home', args=['londo']))
        self.assertEquals(response.status_code, 404)

    def test_no_input(self):
        response = self.client.get(reverse('weatherservice:forecast'))
        print(response.json()['error'])
        print(response)
        print(response)
        print(response)
        print(dir(response))
        self.assertEquals(response.status_code, 400)

    def test_ping_version(self):
        with open('VERSION', 'r') as f:
            version = f.read()

        response = self.client.get(reverse('weatherservice:ping'))
        self.assertEquals(response.json()['version'], version.rstrip())
    
    

