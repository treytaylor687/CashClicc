from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
import re

class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                    )
        return password2


class SignUpForm(UserCreationForm):
    error_messages = {
        'unique_number': ("This phone number is already registered. Please try again."),
    }
    email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=10)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # sets the placeholder key/value in the attrs for a widget
        # when the form is instantiated (so the widget already exists)
        self.fields['username'].widget.attrs['placeholder'] = 'LESS THAN 14 CHARACTERS'
        self.fields['email'].widget.attrs['placeholder'] = 'YOUR EMAIL ADDRESS'
        self.fields['password1'].widget.attrs['placeholder'] = 'AT LEAST 8 CHARACTERS'
        self.fields['password2'].widget.attrs['placeholder'] = 'CONFIRM PASSWORD'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'WE WILL SEND YOU A TEXT TO CONFIRM'

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and Profile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(
                self.error_messages['unique_number'],
                code='unique_number',
            )
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'This email is already registered. Please try again.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u'The passwords do not match. Please try again.')
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(str(username)) > 14:
            raise forms.ValidationError(u'Username too long. Please try again.')
        return username

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')


class PaymentRequestForm(forms.Form):
    error_messages = {
        'balance_error': ("The balance you requested is invalid. Please try again."),
    }
    balance_to_withdraw = forms.IntegerField()
    paypal_email = forms.EmailField(max_length=254)

    def __init__(self, user_bal, *args, **kwargs):
        self.user_balance = user_bal
        super(PaymentRequestForm, self).__init__(*args, **kwargs)
        self.fields['balance_to_withdraw'].label = "Amount (Numbers Only):"

    def clean_balance_to_withdraw(self):
        bal_withdraw = self.cleaned_data.get('balance_to_withdraw')
        if bal_withdraw:
            if bal_withdraw > self.user_balance or bal_withdraw < 0:
                raise forms.ValidationError(
                    self.error_messages['balance_error'],
                    code='balance_error',
                    )
            elif bal_withdraw == 0:
                raise forms.ValidationError(
                    self.error_messages['balance_error'],
                    code='balance_error',
                )
            elif '$' in str(bal_withdraw):
                raise forms.ValidationError(u'Please leave out dollar signs.')
        return bal_withdraw


    def clean_paypal_email(self):
        return self.cleaned_data.get('paypal_email')

class Validate(forms.Form):
    error_messages = {
        'token_invalid': ("The code you entered was invalid. Please try again."),
    }

    login_token = forms.CharField()

    def __init__(self, user_token, *args, **kwargs):
        self.token = user_token
        super(Validate, self).__init__(*args, **kwargs)
        self.fields['login_token'].widget.attrs['placeholder'] = 'ENTER THE CODE WE TEXTED YOU.'

    def clean_login_token(self):
        token = self.cleaned_data.get('login_token')
        if str(self.token) == token:
            return token
        else:
            raise forms.ValidationError(
                self.error_messages['token_invalid'],
                code='token_invalid',
            )

class Contact(forms.Form):
    return_email = forms.EmailField(max_length=254)
    message = forms.CharField(max_length=500)

    def __init__(self, *args, **kwargs):
        super(Contact, self).__init__(*args, **kwargs)
        self.fields['return_email'].label = "Email"

    def clean_return_email(self):
        email = self.cleaned_data.get('return_email')
        return email

    def clean_message(self):
        message = self.cleaned_data.get('message')
        return message
