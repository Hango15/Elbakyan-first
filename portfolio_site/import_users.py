import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_site.settings")
django.setup()

from main.models import Registration
from django.contrib.auth import get_user_model

User = get_user_model()

for reg in Registration.objects.all():
    email = (reg.email or "").strip().lower()
    if not email:
        continue
    if User.objects.filter(email__iexact=email).exists():
        print("Auth user exists, skipping:", email)
        continue

    pw = (reg.password or "").strip()
    if pw.startswith("pbkdf2_") or pw.startswith("argon2") or pw.startswith("bcrypt_"):
        print("Password seems hashed for", email, "- skipping (reset if needed).")
        continue

    username = email.split("@")[0] or "user"
    base = username
    i = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{i}"
        i += 1

    User.objects.create_user(
        username=username,
        email=email,
        password=pw,
        first_name=getattr(reg, "first_name", ""),
        last_name=getattr(reg, "last_name", ""),
    )
    print("Created auth user for", email)
