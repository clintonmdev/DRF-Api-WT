from django.test import SimpleTestCase
from django.urls import reverse, resolve
from weatherservice.views import HomeView, forecast, ping

class TestUrls(SimpleTestCase):
    
    def test_home_url_resolves(self):
        url = reverse('weatherservice:home', args=['paris'])
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_forecast_url_resolves(self):
        url = reverse('weatherservice:forecast')
        print(resolve(url))
        self.assertEqual(resolve(url).func, forecast)

    def test_ping_url_resolves(self):
        url = reverse('weatherservice:ping')
        print(resolve(url))
        self.assertEqual(resolve(url).func, ping)

    def test_temp_conf_url_resolves(self):
        url = reverse('weatherservice:temp_unit', args=['paris', 'celsius'])
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, HomeView)
