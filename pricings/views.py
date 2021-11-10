from django.shortcuts import render
from .models import *
from django.http.response import JsonResponse
import requests

api_key = "AIzaSyBr0ZCQ_NromoQtcplxGQePRaBHZ5cCuZw"

def get_airport_dest(request,airport):
    if "Airport" in airport:
        objs = fixed_pricings.objects.filter(airport_name=airport)
        templist = []
        for i in objs:
            if i.to_or_from not in templist:
                templist.append(i.to_or_from)
        retval = {'a':templist}
    else:
        objs = fixed_pricings.objects.filter(to_or_from=airport)
        templist = []
        for i in objs:
            if i.airport_name not in templist:
                templist.append(i.airport_name)
        retval = {'a':templist}
    return JsonResponse(retval)

def get_price(request,airport,dest,car,ret_check,switchnum=1):
    if "Airport" in airport:
        obj = fixed_pricings.objects.get(airport_name=airport,to_or_from=dest)
    else:
        obj = fixed_pricings.objects.get(airport_name=dest,to_or_from=airport)    
    if ret_check == 'a':
        mul = 2
    else:
        mul = 1
    if car == 'sedan':
        price = '{:10.2f}'.format(obj.sedan_price * mul)
    elif car == 'bus':
        price = '{:10.2f}'.format(obj.bus_price * mul)
    elif car == 'xxlbus':
        price = '{:10.2f}'.format(obj.xxl_bus_price * mul)
    else:
        price = '-'
    if switchnum == 1:
        return JsonResponse({'price':price})
    else:
        return price

def get_price_in_city(request,place_id,place_id2,car):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=place_id:{}&destinations=place_id:{}&key={}".format(place_id,place_id2,api_key)
    response = requests.request("GET", url)
    dist = (float) (response.json()['rows'][0]['elements'][0]['distance']['value']) / 1000
    timet = (float) (response.json()['rows'][0]['elements'][0]['duration']['value']) / 60
    check = False
    if car == 'taxiair':
        obj = variable_pricings.objects.get(pk=1)
        objnum = 1
    elif car == 'taxiairvan':
        obj = variable_pricings.objects.get(pk=2)
        objnum = 2
    elif car == 'taxiairrolstoel':
        obj = variable_pricings.objects.get(pk=3)
        objnum = 3
    else:
        check = True
    if check:
        return JsonResponse(["-"],safe=False)
    price = (obj.km_price * dist) + (obj.minute_price * timet)
    if price <= obj.minimum_price:
        price = obj.minimum_price
    return JsonResponse(["{:10.2f}".format(price),"{:10.2f}".format(dist),"{}".format(timet),"{}".format(objnum)],safe=False)