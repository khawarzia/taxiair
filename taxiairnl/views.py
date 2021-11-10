from django.conf import settings
from django.core.mail.message import EmailMessage
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from pricings.models import *
from pricings.views import get_price
from .models import *
import stripe
from django.contrib import auth

car_names = {
    "sedan" : "Sedan (Eklasse)",
    "bus" : "Bus (Vito)",
    "xxlbus" : "XXL Bus of Rolstoel (Sprinter)",
    "taxiair" : "Taxi Air",
    "taxiairvan" : "Taxi Air Van",
    "taxiairrolstoel" : "Taxi Air Rolstoel"
}

def home(request):
    context = {}
    objs = fixed_pricings.objects.all()
    retval = []
    for i in objs:
        if i.airport_name not in retval:
            retval.append(i.airport_name)
    for i in objs:
        if i.to_or_from not in retval:
            retval.append(i.to_or_from)
    context['objs'] = retval
    return render(request, 'themes/homepage.html', context)

def login0(request):
    return redirect('/login/0')

def login(request,id):
    context = {'forward_id':id}
    if request.method == 'POST':
        try:
            userobj = User.objects.get(username=request.POST['username'])
            if userobj.check_password(request.POST['password']):
                auth.login(request,userobj)
                if id == 0:
                    return redirect('/')
                else:
                    return redirect('/checkout/{}'.format(id))
            else:
                context['message'] = "Invalid Credentials!"
        except:
            context['message'] = "Invalid Credentials!"
    return render(request, 'themes/loginpage.html', context)

def signup0(request):
    return redirect('/signup/0')

def signup(request,id):
    context = {'forward_id':id}
    if request.method == 'POST':
        userobj = user_details()
        userobj.username = request.POST['fullname']
        userobj.email = request.POST['email']
        userobj.number = request.POST['phone']
        userobj.save()
        obj = trip_details.objects.get(pk=id)
        obj.user = userobj
        obj.save()
        return redirect('/checkout/{}'.format(id))
    return render(request, 'themes/signuppage.html', context)
    
def logout(request):
    auth.logout(request)
    return redirect('/')

def gallery(request):
    context = {}
    context['imagecounter'] = list(range(0, 57))
    return render(request, 'themes/gallerypage.html',context)

def leerlingenvervoer(request):
    template = "themes/Leerlingenvervoer.html"
    return render(request,template)

def airportservice(request):
    template = "themes/airportservice.html"
    context = {}
    objs = fixed_pricings.objects.all()
    retval = []
    for i in objs:
        if i.airport_name not in retval:
            retval.append(i.airport_name)
    for i in objs:
        if i.to_or_from not in retval:
            retval.append(i.to_or_from)
    context['objs'] = retval
    return render(request, template, context)

def checkout(request,id):
    context = {}
    obj = trip_details.objects.get(pk=id)
    context['obj'] = obj
    if obj.is_local:
        tempobj = variable_pricings.objects.get(pk=obj.objnum)
        price = (tempobj.km_price * float(obj.dist)) + (tempobj.minute_price * float(obj.timet))
        if price <= tempobj.minimum_price:
            price = tempobj.minimum_price
        context['a'] = "{:10.2f}".format(tempobj.km_price)
        context['b'] = "{:10.2f}".format(tempobj.minute_price)
        context['c'] = "{:10.2f}".format(tempobj.km_price * float(obj.dist))
        context['d'] = "{:10.2f}".format(tempobj.minute_price * float(obj.timet))
        context['price'] = "{:10.2f}".format(price)
    else:
        context['price'] = obj.price
    return render(request, 'themes/checkoutpage.html', context)
    
def airport_form_submit(request):
    if request.method == 'POST':
        obj = trip_details()
        obj.from_loc = request.POST['pick_up_location']
        obj.to_loc = request.POST['drop_off_location']
        obj.date_time = request.POST['booking-time']
        obj.vehicle = car_names[request.POST['car_type']]
        if request.POST['remarks'] != 'Remarks':
            obj.remarks = request.POST['remarks']
        obj.flight_number = request.POST['flight']
        if 'return' in request.POST.keys():
            tempmul = 'a'
            obj.is_return = True
        else:
            tempmul = 'b'
        if 'baby' in request.POST.keys():
            obj.is_babystoel
        obj.price = get_price(request,request.POST['pick_up_location'],request.POST['drop_off_location'],request.POST['car_type'],tempmul,0)
        obj.save()
        return redirect('/signup/{}'.format(obj.id))
    return HttpResponse('Page not accessible!')

def local_form_submit(request):
    if request.method == 'POST':
        obj = trip_details()
        obj.from_loc = request.POST['pick_up_location']
        obj.to_loc = request.POST['drop_off_location']
        obj.date_time = request.POST['booking-time']
        obj.vehicle = car_names[request.POST['car_type']]
        obj.is_local = True
        obj.dist = "{:10.2f}".format(float(request.POST['dist']))
        obj.timet = "{:10.2f}".format(float(request.POST['timet']))
        obj.objnum = request.POST['objnum']
        if request.POST['remarks'] != 'Remarks':
            obj.remarks = request.POST['remarks']
        obj.save()
        return redirect('/signup/{}'.format(obj.id))
    return HttpResponse('Page not accessible!')

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey' : settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe = False)


@csrf_exempt
def create_checkout_session(request,id):
    if request.method == 'GET':
        domain_url = 'http://{}/'.format(request.get_host())
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            obj = trip_details.objects.get(pk = id)
            if obj.is_local:
                tempobj = variable_pricings.objects.get(pk=obj.objnum)
                price = (tempobj.km_price * float(obj.dist)) + (tempobj.minute_price * float(obj.timet))
                if price <= tempobj.minimum_price:
                    price = tempobj.minimum_price
                obj.price = "{:10.2f}".format(price)
                obj.save()
            else:
                price = obj.price
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success/'+str(id)+'?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card','ideal'],
                mode='payment',
                line_items=[
                    {
                        'name': obj.user.username,
                        'quantity': 1,
                        'currency': 'eur',
                        'amount': int(float(price)*100),
                    }
                ]
            )
            template = 'create_checkout_session.html'
            context = {'sessionId' : checkout_session['id']}
            return render(request,template,context)
        except Exception as e:
            return JsonResponse({'error': str(e)})

def success(request,id):
    obj = trip_details.objects.get(pk=id)
    obj.is_paid = True
    obj.save()
    emailpatient = EmailMessage(subject='Ride Booking',body="Your Ride has been Booked. \n Pick Up Location: {} \n Drop Off Location: {} \n Car Type: {}\n Date & Time: {}".format(obj.from_loc ,obj.to_loc, obj.vehicle, obj.date_time),to=[obj.user.email])
    emailpatient.send()
    emaildoctor = EmailMessage(subject='Ride Booking',body="A Ride has been Booked.\n User: {} \n Pick Up Location: {} \n Drop Off Location: {} \n Car Type: {}\n Date & Time: {}".format(obj.user.email,obj.from_loc ,obj.to_loc, obj.vehicle, obj.date_time),to=["khawarzia34@gmail.com"])
    emaildoctor.send()
    template = 'themes/success.html'
    context = {'obj':obj}
    return render(request,template,context)


def error(request):
    template = 'themes/error.html'
    return render(request,template)

def register_driver(request):
    if request.method == 'POST':
        obj = registered_riders()
        obj.full_name = request.POST['name']
        obj.email = request.POST['email']
        obj.phone_number = request.POST['phone']
        obj.dob = request.POST['dob']
        obj.save()
        return render(request,"themes/ridersuccess.html")
    return redirect('/')

def contact_form(request):
    if request.method == 'POST':
        message = "Name : {}\nEmail : {}\Phone Number : {}\nCity : {}\nComments : {}".format(request.POST['name'],
        request.POST['email'],request.POST['phone'],request.POST['city'],request.POST['comment'])
        eobj = EmailMessage(
            subject = "Contacted via TaxiAir webiste",
            body = message,
            to = ["khawarzia34@gmail.com"]
        )
        eobj.send()
        return render(request,"themes/contactsuccess.html")
    return redirect('/')

def adminpage(request):
    template = 'dashboard/dashboard.html'
    context = {}
    context['users'] = User.objects.all()
    context['drivers'] = registered_riders.objects.all()
    context['rides'] = trip_details.objects.filter(is_paid=True)
    return render(request,template,context)