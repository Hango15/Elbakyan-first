from django import forms
from .models import Registration,Login

class Registration_form(forms.ModelForm):
    class Meta:
        model=Registration
        fields=["first_name","Last_name","email","password"]

class Login_form(forms.ModelForm):
    class Meta:
        model=Login
        fields=["email","password"]