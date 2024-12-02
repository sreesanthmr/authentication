from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import redirect
from .forms import CustomUserCreationForm, PhoneNumberRegistrationForm
from django.contrib import messages
import random
from django.core.mail import send_mail
from .models import CustomUser
from django.template.loader import render_to_string
from twilio.rest import Client
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))


def send_verification_email(user):
    otp = generate_otp()
    user.otp = otp
    user.save()

    verification_url = f"http://127.0.0.1:8000/verify/{user.id}/{otp}/"
    subject = "Verify your email"
    html_message = render_to_string(
        "email_template.html", {"user": user, "verification_url": verification_url}
    )

    send_mail(
        subject, "", "sreesanth.mr54@gmail.com", [user.email], html_message=html_message
    )


def verify_email(request, user_id, otp):
    user = get_object_or_404(CustomUser, id=user_id, otp=otp)

    if user is not None:
        user.otp = None
        user.save()
        # messages.success(request, "Your email has been successfully verified.")
        return redirect("/")

    # messages.error(request, "There was an error with your submission.")


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # messages.success(
            #     request, f"Hi {request.user.username}, you are now logged-in"
            # )
            return redirect("home")

        else:
            # messages.warning(request, "Invalid credentials")
            return redirect("/")

    return render(request, "login.html")


@login_required
def home(request):
    return render(request, "home.html")


def custom_logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("/")


def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(user)
            # messages.success(request, "A new OTP has been sent to your email address")
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def send_otp_via_sms(phone_number, otp):
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_="+12495290672",  # Your Twilio phone number
        to=phone_number,
    )


def phone_number_register(request):
    if request.method == "POST":
        form = PhoneNumberRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            otp = generate_otp()
            user.otp = otp
            user.save()
            send_otp_via_sms(user.phone_number, otp)
            return redirect("verify_phone_otp", user_id=user.id)
    else:
        form = PhoneNumberRegistrationForm()
    return render(request, "phone_register.html", {"form": form})


def verify_phone_otp(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":

        otp = request.POST.get("otp")
        if user.otp == otp:

            user.otp = None
            user.save()

            return redirect("phone_login")
        else:
            return render(
                request, "verify_phone_otp.html", {"user": user, "error": "Invalid OTP"}
            )

    return render(request, "verify_phone_otp.html", {"user": user})


def phone_login(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        user = CustomUser.objects.filter(phone_number=phone_number).first()
        if user:
            otp = generate_otp()
            user.otp = otp
            user.save()
            send_otp_via_sms(phone_number, otp)
            return redirect("verify_phone_login_otp", user_id=user.id)
        else:
            return render(
                request, "phone_login.html", {"error": "Phone number not found"}
            )

    return render(request, "phone_login.html")


def verify_phone_login_otp(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        otp = request.POST.get("otp")
        if user.otp == otp:

            user = authenticate(request, otp=otp)

            login(request, user, backend="main_app.backends.PhoneOTPBackend")
            return redirect("home")
        else:
            return render(
                request,
                "verify_phone_login_otp.html",
                {"user": user, "error": "Invalid OTP"},
            )

    return render(request, "verify_phone_login_otp.html", {"user": user})


# def phone_login(request):
#     return render(request,"phone_login.html")


# def verify_otp(request):
#     return render(request, "verify_otp.html")
