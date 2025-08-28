from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import (
    Header,
    Container,
    UserSearch,
    Features,
    Gamesection1,
    Gamesection2,
    Gamesection3,
    Subscriber,
    Shop_section_text,
    Subscribe_text,
    Profile,
    ContanierShop,
    ShopFilter,
    ShopBuysection,
    Game,
    Product,
    Genre,
    Tag,
    Review,
    ContactMessage

)

User = get_user_model()

admin.site.register(Header)
admin.site.register(Features)
admin.site.register(Gamesection1)
admin.site.register(Gamesection2)
admin.site.register(Gamesection3)
admin.site.register(Shop_section_text)
admin.site.register(Subscribe_text)
admin.site.register(ContanierShop)
admin.site.register(ShopFilter)
admin.site.register(Product)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Review)

# Inline for Games inside a Shop Section
class GameInline(admin.TabularInline):
    model = Game
    extra = 1  # how many empty forms to show
    fields = ('gamename', 'gamegenre', 'pricetextoriginal', 'pricetextlowered', 'gameimg')

# Shop Section admin with inline Games
class ShopBuysectionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [GameInline]

# Register models
admin.site.register(ShopBuysection, ShopBuysectionAdmin)
admin.site.register(Game)

@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    search_fields = ('h2text', 'h6text')

@admin.register(UserSearch)
class UserSearchAdmin(admin.ModelAdmin):
    list_display = ('search_term', 'user', 'ip_address', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('search_term', 'user__username')
    date_hierarchy = 'created_at'

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at")
    list_filter = ('email', 'subscribed_at')
    search_fields = ("email",)

# Optional: register Profile so you can edit extra fields in admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscribe')
    search_fields = ('user__username', 'email')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "email", "subject", "created_at")
    search_fields = ("name", "surname", "email", "subject", "message")
    list_filter = ("created_at",)