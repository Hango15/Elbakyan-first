from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout,get_user_model
from django.db import DatabaseError
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Header, Container, UserSearch,Features,Gamesection1,Gamesection2,Gamesection3,Subscriber,Profile,HeaderShop,ContanierShop,ShopFilter

import logging
logger = logging.getLogger(__name__)


def index(request):
    """
    Render the homepage with the first header and container settings.
    """
    settinghead = Header.objects.first()
    settingcontainer = Container.objects.first()
    settingfeature=Features.objects.first()
    settinggames=Gamesection1.objects.first()
    settinggames2=Gamesection2.objects.first()
    settinggames3=Gamesection3.objects.first()

    context = {
        "settinghead": settinghead,
        "settingcontainer": settingcontainer,
        "settingfeature":settingfeature,
        "settinggames":settinggames,
        "settinggames2":settinggames2,
        "settinggames3":settinggames3,
    }
    return render(request, "index.html", context)


@require_POST
def handle_search(request):
    """
    Handles search form submissions.
    Saves the search term into UserSearch, returns success/failure messages.
    Works with both normal POST requests and AJAX (fetch).
    """
    search_term = request.POST.get("searchKeyword", "").strip()

    if not search_term:
        # Empty search
        logger.warning("Empty search submitted")
        messages.warning(request, "Please enter a search term")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {"status": "error", "message": "Empty search term"},
                status=400,
            )
        return redirect("index")

    try:
        # Save search to DB
        UserSearch.objects.create(
            search_term=search_term,
            ip_address=request.META.get("REMOTE_ADDR"),
            user=request.user if request.user.is_authenticated else None,
        )
        logger.info(
            f"Search saved: '{search_term}' "
            f"(user={request.user}, ip={request.META.get('REMOTE_ADDR')})"
        )

    except DatabaseError as e:
        logger.exception("Database error while saving search")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {"status": "error", "message": "Database error"},
                status=500,
            )
        messages.error(request, "Could not record search. Please try again.")
        return redirect("index")

    # Success response
    messages.success(request, f"Search recorded for: {search_term}")
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {"status": "success", "message": f"Search recorded for: {search_term}"}
        )

    return redirect("index")

def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            Subscriber.objects.get_or_create(email=email)
            messages.success(request, "Thanks for subscribing!")
        else:
            messages.error(request, "Please enter a valid email")
    return redirect("index")  # change "index" to your homepage


def shop(request):
    shophead=HeaderShop.objects.first()
    shopcontanier=ContanierShop.objects.first()
    shopfilter=ShopFilter.objects.first()

    shopcontext={
        "shophead":shophead,
        "shopcontanier":shopcontanier,
        "shopfilter":shopfilter,
    }
    return render(request, "shop.html",shopcontext)

def product_details(request, id):
    # Կարող ես տվյալները բազայից բեռնել, բայց հիմա կսարքենք dummy:
    context = {"product_id": id}
    return render(request, "product_details.html", context)

def contact(request):
    return render(request, "contact.html")


User = get_user_model()

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name  = request.POST.get("last_name", "").strip()
        email      = request.POST.get("email", "").strip().lower()
        password   = request.POST.get("password", "")

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, "register.html")

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "An account with that email already exists.")
            return render(request, "register.html")

        # create a unique username from email local part
        base = email.split("@")[0] or "user"
        username = base
        i = 1
        while User.objects.filter(username=username).exists():
            username = f"{base}{i}"
            i += 1

        # create the Django auth user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # create a Profile automatically
        Profile.objects.create(user=user)

        messages.success(request, "Account created — you can now log in.")
        return redirect("login")

    return render(request, "register.html")



def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = None
        if email and password:
            try:
                user_obj = User.objects.get(email__iexact=email)
                # authenticate using the user's username (Django's default)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect("index")
            else:
                messages.error(request, "This account is inactive.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "login.html")