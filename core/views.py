from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
import paypalrestsdk 
from django.core.mail import send_mail
from .models import *
from .forms import CreateUserForm, UserProfileForm, ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
import yagmail
from django.contrib import messages
from .forms import CreateUserForm, UserProfileForm
from core import services
from .models import Cryptocurrency
from .forms import CreateUserForm, UserProfileForm
from . utils import cookieCart


def home_view(request):
    return render(request, 'core/home.html')



def registerPage(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = user.username
            messages.success(request, 'Account created for ' + username)
            return redirect('login')

    else:
        user_form = CreateUserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'core/register.html', context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request, 'core/login.html')
    context = {}
    return render(request, 'core/login.html')


def logoutView(request):
    logout(request)
    return redirect('home')


def send_email(subject, contents, to_email):
    yag = yagmail.SMTP('cryptosphereinnovators@gmail.com', 'crypto@123')
    yag.send(to=to_email, subject=subject, contents=contents)


def forgot_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='core/reset_email_template.html',
                subject_template_name='core/reset_subject_template.txt',
                from_email='cryptosphereinnovators@gmail.com',
            )
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'core/forgot_password_template.html', {'form': form})


def blockchain(request):
    return render(request, 'core/blockchain.html')


def Markettrends(request):
    return render(request, 'core/Markettrends.html')


def tech_view(request):
    # Add any context data if needed
    return render(request, 'core/technology.html')


def invest_view(request):
    # Add any context data if needed
    return render(request, 'core/investment.html')


def index(request):
    selected_currency = request.GET.get('currency', 'USD')
    request.session['selected_currency'] = selected_currency
    # Fetch cryptocurrency data in the selected currency
    cryptos = services.get_cryptocurrency_data(currency=selected_currency)

    try:
        user_profile = UserProfile.objects.get(user=request.user)
        profile_pic = user_profile.profile_pic
    except UserProfile.DoesNotExist:
        profile_pic = None

    # Pass the list of cryptocurrencies to the template
    return render(request, 'core/home1.html', {'cryptos': cryptos,
                                               'profile_pic': profile_pic,
                                               'selected_currency': selected_currency})


def crypto_detail(request, symbol):
    # Here you can fetch detailed data based on the symbol
    # detailed_data = get_detailed_data(symbol)  # Implement this function

    selected_currency = request.session.get('selected_currency', 'USD')
    crypto_data = services.get_cryptocurrency_data(currency=selected_currency)
    data = next((item for item in crypto_data if item.symbol == symbol), None)

    if not data:
        return render(request, 'core/crypto_detail.html', {
            'error': 'Chart data is not available.',
            'selected_currency': selected_currency
        })
    chart_path = services.get_crypto_chart(symbol, data, selected_currency)
    market_cap_chart_path = services.getsupply_chart(symbol, data, selected_currency)

    # Check if the charts are generated and pass them to the template
    if chart_path and market_cap_chart_path:
        return render(request, 'core/crypto_detail.html', {
            'chart_path': chart_path,
            'market_cap_chart_path': market_cap_chart_path,
            'selected_currency': selected_currency,
            'crypto': data
            # 'data': detailed_data  # Add or modify as needed
        })
    else:
        return render(request, 'core/crypto_detail.html', {
            'error': 'Chart data is not available.',
            'selected_currency': selected_currency,
            'crypto': data

        })

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)  # Save form data but don't commit to the database yet
            form_instance.save()  # Save to database

            # Sending email notification
            subject = 'New Contact Form Submission'
            message = f'You have a new contact form submission:\n\nName: {form_instance.name}\nEmail: {form_instance.email}\nMessage: {form_instance.message}'
            from_email = 'cryptosphereinnovators@gmail.com'  # Replace with your email
            to_email = 'cryptosphereinnovators@gmail.com'  # Replace with admin email
            send_mail(subject, message, from_email, [to_email])

            return redirect('thank_you')  # Redirect to a thank you page or any other desired URL

    else:
        form = ContactForm()

    return render(request, 'core/contact_us.html', {'form': form})

def thank_you(request):
    return render(request, 'core/thank_you.html')


def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order ={'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    products=Product.objects.all()
    selected_currency = request.session.get('selected_currency', 'USD')
    crypto_data = services.get_cryptocurrency_data(currency=selected_currency)
    product_to_symbol = {
        'Tether': 'USDT',
        'Dash': 'DOGE',
        'Litecoin': 'LTC',
        'BitCoin': 'BTC',
        'Monero': 'XMR',
        'Altcoins': 'AVAX'
    }
    product_price_map = {}

    for product in products:
        symbol = product_to_symbol.get(product.name)
        if symbol:
            # Find the corresponding cryptocurrency instance
            crypto = next((c for c in crypto_data if c.symbol == symbol), None)
            if crypto:
                product_price_map[product.name] = crypto.price
            else:
                product_price_map[product.name] = None  # or some default value

    context = {'products':products, 'cartItems':cartItems,'product_price_map': product_price_map}
    #print(context) 
    return render(request, 'core/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('Cart:', cart)
        items = []
        order ={'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

        for i in cart:
            try:
                cartItems += cart[i]["quantity"]

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]["quantity"])

                order['get_cart_total'] +=total
                order['get_cart_items'] +=cart[i]["quantity"]

                item = {
                    'product': {
                        'id':product.id,
                        'name' : product.name,
                        'price' :product.price,
                        'imageURL':product.imageURL,
                        },
                    'quantity': cart[i]["quantity"],
                    'get_total':total
                    }
                items.append(item)
            except:
                pass

            

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'core/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order ={'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'core/checkout.html', context)

def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     print('Action:', action)
     print('productId:', productId)
     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)
     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product) 

     if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
     orderItem.save()
     if orderItem.quantity <=0:
        orderItem.delete()

     return JsonResponse('Item was added', safe=False)

# def processOrder(request):
#     body_unicode = request.body.decode('utf-8')
#     body = json.loads(body_unicode)
#
#
#     # Assuming you are passing the user's ID in the request
#     user_id = body['user_id']
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         name = data['form']['name']
#         email = data['form']['email']
#         total = data['form']['total']
#
#
#
#
#         # Save the order details to OrderHistory model
#         order_history = OrderHistory.objects.create(
#             name=name,
#             email=email,
#             price=total
#         )
#
#     # Update the order status to complete
#     order = Order.objects.get(customer__user__id=user_id, complete=False)
#     order.complete = True
#     order.save()
#
#     # Clear the user's cart
#     order.orderitem_set.all().delete()
#
#     return JsonResponse('Payment Complete', safe=False)

@login_required
def orderhistory(request):
    order_history_data = OrderHistory.objects.all().order_by('-transaction_date')
    context = {'order_history': order_history_data}
    print(order_history_data)  # Add this line to print data to console
    return render(request, 'core/orderhistory.html', context)

@csrf_exempt
def processOrder(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['form']['name']
        email = data['form']['email']
        total = data['form']['total']

        # Print values for debugging
        print('Name:', name)
        print('Email:', email)
        print('Total:', total)

        # Save the order details to OrderHistory model
        order_history = OrderHistory.objects.create(
            name=name,
            email=email,
            price=total
        )

        return JsonResponse({'message': 'Payment Complete'}, safe=False)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400, safe=False)


