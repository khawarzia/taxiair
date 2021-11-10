from django.urls import path,include
from django.urls.resolvers import URLPattern
from . import views


urlpatterns = [
    path('get-airport-dest/<str:airport>',views.get_airport_dest),
    path('get-price/<str:airport>/<str:dest>/<str:car>/<str:ret_check>',views.get_price),
    path('get-price-in-city/<str:place_id>/<str:place_id2>/<str:car>',views.get_price_in_city)
]