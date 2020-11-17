from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import json
import requests

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


appid = settings.API_KEY

class IndexView(APIView):
    def get(self, request):
        data = {
            'Title': 'Weather service app',
            'Instructions': 'Login then go to forecast/(city name) and there you go',
            'Extra': 'change the temperature unit by going to forecast/(city name)/(temperature unit)'
        }
        return Response(data)


class HomeView(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Base unit is Kelvin
    def temp_converter(flaot, new_temp_unit):
        if new_temp_unit == 'celsius':
            result = flaot - 273.15
            return result
        elif new_temp_unit == 'farenheit':
            result = (temp - 273.15) * 9/5 + 32
            return result
        elif new_temp_unit == 'kelvin' :
            result = temp
            return result

    @method_decorator(cache_page(60*15))
    def get(self, request, city, temp_unit='celsius', format=None, *args, **kwargs):
        authentication_classes = [SessionAuthentication, BasicAuthentication]
        try:
            r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}'.format(city=city, appid=appid))
            r_content = r.json()

            r_temp = r_content['main']['temp']
            if temp_unit == 'celsius':
                final_temp = r_temp - 273.15
            elif temp_unit == 'farenheit':
                final_temp = (r_temp - 273.15) * 9/5 + 32
            elif temp_unit == 'kelvin' :
                final_temp = r_temp
        
            data = {
                    'clouds': r_content['weather'][0]['description'],
                    'humidity': str(r_content['main']['humidity']) + "%" ,
                    'pressure': str(r_content['main']['pressure']) + " hPa",
                    'temperature': str( "%.1f" % final_temp) + temp_unit[0].upper(),
                }
            status = 200
        except UnboundLocalError:
            data = {
                "error": str(temp_unit) + " is not a valid temperature unit, please choose between celsius, farenheit and kelvin " ,
                "error_code": "temperature unit not found"
                }
            status=404
        except KeyError:
            data = {
                    "error": "Cannot find city " + str(city),
                    "error_code": "city not found"
            }
            status=404
        except Exception:
            data = {
                "error": "something went wrong",
                "error_code": "internal server error"
            }
            status=500
    
        finally:
            if r.status_code == 401:
                data = 'Invalid API key'
                return JsonResponse(data, safe=False, status=r.status_code)

        return JsonResponse(data, json_dumps_params={'indent': ' '}, safe=False, status=status)



def forecast(requests):
    data = {
            "error": "no city provided",
            "error_code": "invalid request"
    }
    return JsonResponse(data,json_dumps_params={'indent': ' '}, safe=False, status=400, )



def ping(request):
    try:
        with open('VERSION', 'r') as f:
            version = f.read()
        
        print(version)
        data = {
            "name": "weatherservice",
            "status": "ok",
            "version": version.rstrip()
        }
    except Exception:
        data = "Something went wrong ..."

    return JsonResponse(data,json_dumps_params={'indent': ' '}, safe=False)


