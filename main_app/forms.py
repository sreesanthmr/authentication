from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "input", "placeholder": "Enter Email"}),
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "Enter Username"}
        )
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "Enter Password"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "Enter Password Again"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PhoneNumberRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "Enter Username"}
        )
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "Enter Phone Number"}
        )
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()  
        if not user.email:
            user.email = f'{user.phone_number}@email.com'
        if commit:
            user.save()
        return user
