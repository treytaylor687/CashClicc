from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from paypal.standard.forms import PayPalPaymentsForm
from cashclicc.core.models import Game, MessageClient, Donation
from cashclicc.core.forms import SignUpForm, PaymentRequestForm, Validate, Contact
from .forms import SetPasswordForm
from django.contrib import messages
from random import randint
from django.core.mail import send_mail
from ..settings import DEFAULT_FROM_EMAIL
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import timedelta
import os

def home(request):
    #if request.user.is_authenticated(
    # ):
    #    return redirect('/games/')

    if request.META.get('HTTP_REFERER') == "https://www.cashclicc.com/login/":
        return redirect('/games/')
    elif request.user.is_authenticated():
        profile = request.user.profile
        donation = Donation.objects.all()[0]
        context = {'profile': profile, 'donation': donation}
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')

    #return render(request, 'landing.html')



@login_required()
def account(request):
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'account.html', context)


def store(request):
    single_token_form = {
        "business": "info@cashclicc.com",
        "amount": "4.99",
        "item_name": "10 Tokens",
        "invoice": randint(1111111111, 9999999999),
        "notify_url": "cashclicc.com" + reverse('paypal-ipn'),
        "return_url": "https://www.cashclicc.com",
        "cancel_return": "https://www.cashclicc.com/store",
        "custom": request.user.username,
    }
    five_token_form = {
        "business": "info@cashclicc.com",
        "amount": "9.99",
        "item_name": "25 Tokens",
        "invoice": randint(1111111111, 9999999999),
        "notify_url": "cashclicc.com" + reverse('paypal-ipn'),
        "return_url": "https://www.cashclicc.com",
        "cancel_return": "https://www.cashclicc.com/store",
        "custom": request.user.username,
    }
    ten_token_form = {
        "business": "info@cashclicc.com",
        "amount": "16.99",
        "item_name": "50 Tokens",
        "invoice": randint(1111111111, 9999999999),
        "notify_url": "cashclicc.com" + reverse('paypal-ipn'),
        "return_url": "https://www.cashclicc.com",
        "cancel_return": "https://www.cashclicc.com/store",
        "custom": request.user.username,
    }
    tf_token_form = {
        "business": "info@cashclicc.com",
        "amount": "29.99",
        "item_name": "100 Tokens",
        "invoice": randint(1111111111, 9999999999),
        "notify_url": "cashclicc.com" + reverse('paypal-ipn'),
        "return_url": "https://www.cashclicc.com",
        "cancel_return": "https://www.cashclicc.com/store",
        "custom": request.user.username,
    }
    fifty_token_form = {
        "business": "info@cashclicc.com",
        "amount": "49.99",
        "item_name": "250 Tokens",
        "invoice": randint(1111111111, 9999999999),
        "notify_url": "cashclicc.com" + reverse('paypal-ipn'),
        "return_url": "https://www.cashclicc.com",
        "cancel_return": "https://www.cashclicc.com/store",
        "custom": request.user.username,
    }
    hundred_token_form = {
        "business": "info@cashclicc.com",
        "amount": "74.99",
        "item_name": "500 Tokens",
        "invoice": randint(1111111111, 9999999999),
        "notify_url": "cashclicc.com" + reverse('paypal-ipn'),
        "return_url": "https://www.cashclicc.com",
        "cancel_return": "https://www.cashclicc.com/store",
        "custom": request.user.username,
    }

    single = PayPalPaymentsForm(initial=single_token_form)
    five = PayPalPaymentsForm(initial=five_token_form)
    ten = PayPalPaymentsForm(initial=ten_token_form)
    tf = PayPalPaymentsForm(initial=tf_token_form)
    fifty = PayPalPaymentsForm(initial=fifty_token_form)
    hund = PayPalPaymentsForm(initial=hundred_token_form)

    context = {
        "single": single,
        "five": five,
        "ten": ten,
        "tf": tf,
        "fifty": fifty,
        "hund": hund,
    }

    return render(request, 'store.html', context)

@login_required()
def game_page(request, game_id):
    game_object = Game.objects.filter(id=game_id)[0]
    context = {'game_object': game_object}
    if request.GET.get(str(game_object.pk)):
        if request.user.profile.get_tokens() > 0:
            if game_object.get_top_user() != request.user.username and game_object.status == 1:
                username = str(User.objects.filter(username=request.user.profile.user)[0])
                Donation.objects.all()[0].increase_donations()
                game_object.current_top_user = username
                time_d = game_object.end_time - game_object.current_time
                if time_d.seconds < 10:
                    game_object.end_time += timedelta(seconds=(10.5 - time_d.seconds))
                game_object.save()
                if Game.objects.filter(id=game_id)[0].current_top_user == username:
                    request.user.profile.use_token()
                return redirect('/games/' + str(game_object.pk) + '/')
            return redirect('/games/' + str(game_object.pk) + '/')
        else:
            return redirect('/store/')
    else:
        return render(request, 'game_page.html', context)



def games(request):
    game_objects = Game.objects.all().order_by('end_time')
    context = {'games': game_objects}
    return render(request, 'games.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            return_email = form.clean_return_email()
            message = form.clean_message()
            subject = 'Message from: ' + return_email
            success_message = 'Your message has been received! We will respond as soon as possible.'
            send_mail(subject, message, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL], fail_silently=False)
            return render(request, 'contact.html', {'form': form, 'success': success_message})
    else:
        form = Contact()
    return render(request, 'contact.html', {'form': form})

@login_required()
def withdraw(request):
    if request.method == 'POST':
        form = PaymentRequestForm(request.user.profile.balance, request.POST)
        if form.is_valid():
            balance = str(form.clean_balance_to_withdraw())
            request.user.profile.balance -= form.clean_balance_to_withdraw()
            request.user.save()
            to_address = form.clean_paypal_email()
            subject = 'Balance Request: $' + balance
            success_message = 'Your withdrawal request has been received. We will process your payment as soon as possible.'
            email = balance + " requested to " + to_address
            send_mail(subject, email, DEFAULT_FROM_EMAIL, [DEFAULT_FROM_EMAIL], fail_silently=False)
            return render(request, 'withdraw.html', {'form': form, 'success': success_message})
    else:
        form = PaymentRequestForm(request.user.profile.balance)
    return render(request, 'withdraw.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        confirmation = MessageClient()
        validation_token = confirmation.generate_token()
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.is_active = False
            user.profile.phone_number = form.clean_phone_number()
            user.profile.set_validation_token(validation_token)
            user.save()
            confirmation.send_message(
                "Here Is Your Cash Clicc Confirmation Code: " + str(validation_token),
                "+1" + str(user.profile.phone_number)
            )
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=user.username, password=raw_password)
            #login(request, user)
            redirect_url = '/activate/' + str(user.pk)
            return redirect(redirect_url)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def refresh_game(request, game_id):
    game_object = Game.objects.filter(id=game_id)[0]
    current_time = game_object.time_remaining()
    if game_object.status == 1 and current_time != "quit":
        game_object.update_current_time()
        time_delta = game_object.end_time - game_object.current_time
        user = game_object.get_top_user()
        if time_delta.seconds <= 10:
            response = "red" + ":" + str(current_time) + ":" + user
        elif time_delta.seconds <= 3600:
            response = "orange" + ":" + str(current_time) + ":" + user
        else:
            response = str(current_time) + ":" + user
        return HttpResponse(response)
    return HttpResponse("quit")


def reset_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password2']
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password has been reset.')
            return redirect('home')
    else:
        form = SetPasswordForm()
    return render(request, 'reset.html', {'form': form})


def activate(request, user_id):
    user = User.objects.filter(pk=user_id)[0]
    """"""
    if request.method == 'POST':
        form = Validate(user.profile.get_validation_token(), request.POST)
        if form.is_valid():
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('/games/')
        else:
            redirect_url = '/activate/' + str(user.pk)
            return redirect(redirect_url)
    else:
        form = Validate(user.profile.get_validation_token())
    return render(request, 'validate.html', {'form': form})


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

def tutorial(request):
    if request.user.is_authenticated():
        profile = request.user.profile
        context = {'profile': profile}
        return render(request, 'tutorial.html', context)
    else:
        return render(request, 'tutorial.html')

def donations(request):
    return HttpResponse(Donation.objects.all()[0].get_total_donation())
