from django import forms
from .models import ContactMessage,Game


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'surname', 'email', 'subject', 'message']

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['gamename', 'gamegenre', 'gameimg', 'pricetextoriginal', 'pricetextlowered', 'shop_section']