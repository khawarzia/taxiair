from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/<int:id>', views.login, name='login'),
    path('login', views.login0, name='login0'),
    path('signup/<int:id>', views.signup, name='signup'),
    path('signup', views.signup0, name='signup0'),
    path('logout', views.logout, name='logout'),
    path('gallery', views.gallery, name='gallery'),
    path('checkout/<int:id>', views.checkout, name='checkout'),

    path('airport-form-submit', views.airport_form_submit, name='airport-form-submit'),
    path('local-form-submit', views.local_form_submit, name='local-form-submit'),

    path('config/',views.stripe_config),
    path('create-checkout-session/<int:id>', views.create_checkout_session, name="create-checkout-session"), 
    path('success/<int:id>', views.success , name = 'SuccessPayment') ,
    path('error', views.error , name = 'ErrorPayment') ,

    path('register-driver', views.register_driver, name='register-driver'),
    path('contact-form', views.contact_form, name='contact-form'),

    path('adminpage', views.adminpage, name='adminpage'),
    path('leerlingenvervoer', views.leerlingenvervoer, name="leerlingenvervoer"),
    path('airportservice', views.airportservice, name="airport-service"),

]