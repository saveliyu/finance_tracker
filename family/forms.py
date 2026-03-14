from django import forms
from .models import FamilyInvite


class InviteForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'XXXXXXXX', 'maxlength': 8, 'autofocus': True}))
