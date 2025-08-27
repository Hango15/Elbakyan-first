from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Header, Container, UserSearch, Features, Gamesection1, Gamesection2, Gamesection3, Subscriber, Profile,HeaderShop,ContanierShop

User = get_user_model()

admin.site.register(Header)
admin.site.register(Features)
admin.site.register(Gamesection1)
admin.site.register(Gamesection2)
admin.site.register(Gamesection3)
admin.site.register(HeaderShop)
admin.site.register(ContanierShop)
# Remove admin.site.register(User) — auth app already has User admin

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
