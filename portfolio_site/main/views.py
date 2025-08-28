from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout,get_user_model
from django.db import DatabaseError
from django.views.decorators.http import require_POST
from django.utils import timezone
from .forms import ContactForm
from .models import (
    Header,
    Container,
    UserSearch,
    Features,
    Gamesection1,
    Gamesection2,
    Gamesection3,
    Subscriber,
    Subscribe_text,
    Shop_section_text,
    Profile,
    ContanierShop,
    ShopFilter,
    ShopBuysection,
    Game,
)

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
    settingsubtext=Subscribe_text.objects.first()
    settingshopsectiontext=Shop_section_text.objects.first()

    context = {
        "settinghead": settinghead,
        "settingcontainer": settingcontainer,
        "settingfeature":settingfeature,
        "settinggames":settinggames,
        "settinggames2":settinggames2,
        "settinggames3":settinggames3,
        "settingsubtext":settingsubtext,
        "settingshopsectiontext":settingshopsectiontext
    }
    return render(request, "index.html", context)

def shop(request):
    settinghead = Header.objects.first()
    shopcontanier = ContanierShop.objects.first()
    shopfilter = ShopFilter.objects.first()

    sections = ShopBuysection.objects.prefetch_related('games').all()

    shopcontext = {
        "settinghead": settinghead,
        "shopcontanier": shopcontanier,
        "shopfilter": shopfilter,
        "sections": sections,
    }
    return render(request, "shop.html", shopcontext)

def product_details(request, id):
    # Fetch the product
    product = get_object_or_404(Game, id=id)

    # Related games: pick 4 games from the same genre, excluding current
    # Adjust based on your model's field names: 'gamegenre' or ManyToMany
    if hasattr(product, 'gamegenre'):
        related_games = Game.objects.filter(gamegenre=product.gamegenre).exclude(id=product.id)[:4]
    else:
        related_games = []

    # Header for nav menu
    settinghead = Header.objects.first()

    context = {
        "product": product,
        "settinghead": settinghead,
        "related_games": related_games,
    }
    return render(request, "product_details.html", context)

def contact(request):
    settinghead = Header.objects.first()
    context={
        "settinghead":settinghead,
    }

    return render(request, "contact.html",context)

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


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect("contact")  # reload the page after saving
    else:
        form = ContactForm()
    
    return render(request, "contact.html", {"form": form})