from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#Index.html

# ---------- Header & Content Models ----------
class Header(models.Model):
    logo = models.ImageField(upload_to='logo/', blank=True)
    texthtml1 = models.CharField(max_length=200, default="Home")
    texthtml2 = models.CharField(max_length=200, default="Our shop")
    texthtml3 = models.CharField(max_length=200, default="Product details")
    texthtml4 = models.CharField(max_length=200, default="Contact us")
    signuptext = models.CharField(max_length=200, default="Sign up")

    def __str__(self):
        return "Header Configuration"

class Container(models.Model):
    h2text = models.CharField(max_length=200, default="WELCOME TO LUGX")
    h6text = models.CharField(max_length=200, default="BEST GAMING SITE EVER")
    ptext = models.TextField()
    pricetext = models.CharField(max_length=200, default="$22")
    offertext = models.CharField(max_length=200, default="-40%")
    buttontext = models.CharField(max_length=200, default="SEARCH")
    Gameimg = models.ImageField(upload_to='Gamesimg/', blank=True)

# ---------- User-related ----------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribe = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class UserSearch(models.Model):
    search_term = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='searches'
    )

    class Meta:
        verbose_name = "User Search"
        verbose_name_plural = "User Searches"
        ordering = ['-created_at']

    def __str__(self):
        return f"Search: {self.search_term} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"

# ---------- Subscriber ----------
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
# ---------- Subscribe text ----------

class Subscribe_text(models.Model):
    h6redtext=models.CharField(max_length=200)
    h2text=models.CharField(max_length=400)
    h2bluetext=models.CharField(max_length=100)
    buttontext=models.CharField(max_length=200)

# ---------- Shop section text ----------
class Shop_section_text(models.Model):
    
    h6redtext=models.CharField(max_length=200)
    h2text=models.CharField(max_length=400)
    h2bluetext=models.CharField(max_length=100)
    ptext=models.TextField()
    buttontext=models.CharField(max_length=200)


# ---------- Feature & Game Sections ----------
class Features(models.Model):
    featureimg1 = models.ImageField(upload_to='Featureimg/', blank=True)
    featuretext1 = models.CharField(max_length=200, default="FREE STORAGE")
    featureimg2 = models.ImageField(upload_to='Featureimg/', blank=True)
    featuretext2 = models.CharField(max_length=200, default="USER MORE")
    featureimg3 = models.ImageField(upload_to='Featureimg/', blank=True)
    featuretext3 = models.CharField(max_length=200, default="REPLY READY")
    featureimg4 = models.ImageField(upload_to='Featureimg/', blank=True)
    featuretext4 = models.CharField(max_length=200, default="EASY LAYOUT")

class Gamesection1(models.Model):
    h6redtext=models.CharField(max_length=200, default="TRENDING")
    h2text=models.CharField(max_length=200, default="Trending Games")

    buttontext=models.CharField(max_length=200, default="View All")

    pricetextoriginal1=models.CharField(max_length=200)
    pricetextlowered1=models.CharField(max_length=200)
    gamename1=models.CharField(max_length=200)
    gamegenre1=models.CharField(max_length=200)
    gameimg1=models.ImageField(upload_to='Gamesimg/',blank=True)

    pricetext2=models.CharField(max_length=200)
    gamename2=models.CharField(max_length=200)
    gamegenre2=models.CharField(max_length=200)
    gameimg2=models.ImageField(upload_to='Gamesimg/',blank=True)

    pricetextoriginal3=models.CharField(max_length=200)
    pricetextlowered3=models.CharField(max_length=200)
    gamename3=models.CharField(max_length=200)
    gamegenre3=models.CharField(max_length=200)
    gameimg3=models.ImageField(upload_to='Gamesimg/',blank=True)

    pricetext4=models.CharField(max_length=200)
    gamename4=models.CharField(max_length=200)
    gamegenre4=models.CharField(max_length=200)
    gameimg4=models.ImageField(upload_to='Gamesimg/',blank=True)

class Gamesection2(models.Model):
    h6redtext=models.CharField(max_length=200, default="TOP GAMES")
    h2text=models.CharField(max_length=200, default="Most played")

    buttontext1=models.CharField(max_length=200, default="View All")
    buttontext2=models.CharField(max_length=200, default="Explore")

    gamename1=models.CharField(max_length=200)
    gamegenre1=models.CharField(max_length=200)
    gameimg1=models.ImageField(upload_to='Gamesimg/',blank=True)

    gamename2=models.CharField(max_length=200)
    gamegenre2=models.CharField(max_length=200)
    gameimg2=models.ImageField(upload_to='Gamesimg/',blank=True)

    gamename3=models.CharField(max_length=200)
    gamegenre3=models.CharField(max_length=200)
    gameimg3=models.ImageField(upload_to='Gamesimg/',blank=True)

    gamename4=models.CharField(max_length=200)
    gamegenre4=models.CharField(max_length=200)
    gameimg4=models.ImageField(upload_to='Gamesimg/',blank=True)

    gamename5=models.CharField(max_length=200)
    gamegenre5=models.CharField(max_length=200)
    gameimg5=models.ImageField(upload_to='Gamesimg/',blank=True)

    gamename6=models.CharField(max_length=200)
    gamegenre6=models.CharField(max_length=200)
    gameimg6=models.ImageField(upload_to='Gamesimg/',blank=True)


class Gamesection3(models.Model):
    h6redtext=models.CharField(max_length=200, default="CATEGORIES")
    h2text=models.CharField(max_length=200, default="Top Categories")

    gamegenre1=models.CharField(max_length=200)
    gameimg1=models.ImageField(upload_to='Gamesimg/',blank=True)

    gamegenre2=models.CharField(max_length=200)
    gameimg2=models.ImageField(upload_to='Gamesimg/',blank=True)

    gamegenre3=models.CharField(max_length=200)
    gameimg3=models.ImageField(upload_to='Gamesimg/',blank=True)

    gamegenre4=models.CharField(max_length=200)
    gameimg4=models.ImageField(upload_to='Gamesimg/',blank=True)

    gamegenre5=models.CharField(max_length=200)
    gameimg5=models.ImageField(upload_to='Gamesimg/',blank=True)



#Shop.html

# ---------- & Content Models ---------

class ContanierShop(models.Model):
    bigtext=models.CharField(max_length=200)
    smalltext1=models.CharField(max_length=200)
    smalltext2=models.CharField(max_length=200)
#---------- Filter ----------

class ShopFilter(models.Model):
    filtertext1=models.CharField(max_length=200)
    filtertext2=models.CharField(max_length=200)
    filtertext3=models.CharField(max_length=200)
    filtertext4=models.CharField(max_length=200)

#---------- Buy section ----------

class ShopBuysection(models.Model):
    title = models.CharField(max_length=200, help_text="Section name (e.g. Top Discounts, Bestsellers)")

    def __str__(self):
        return self.title


class Game(models.Model):
    shop_section = models.ForeignKey(
        ShopBuysection, 
        on_delete=models.CASCADE, 
        related_name="games"
    )
    gamename = models.CharField(max_length=200)
    gamegenre = models.CharField(max_length=200)
    pricetextoriginal = models.CharField(max_length=200)
    pricetextlowered = models.CharField(max_length=200)
    gameimg = models.ImageField(upload_to="Gamesimg/", blank=True)

    def __str__(self):
        return self.gamename

#PRODUCT_DETAILS.HTML

class Genre(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    game_id = models.CharField(max_length=20)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    long_description = models.TextField(blank=True)
    original_price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    genre = models.ManyToManyField(Genre)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


#Contact.html

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.subject}"