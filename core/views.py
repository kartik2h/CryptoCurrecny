from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
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

    selected_currency = request.GET.get('currency', 'USD')
    crypto_data = services.get_cryptocurrency_data(selected_currency)
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
            'selected_currency': selected_currency
            # 'data': detailed_data  # Add or modify as needed
        })
    else:
        return render(request, 'core/crypto_detail.html', {
            'error': 'Chart data is not available.',
            'selected_currency': selected_currency
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