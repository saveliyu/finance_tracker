from django import forms
from .models import FamilyInvite, FamilyMember


class InviteForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'XXXXXXXX', 'maxlength': 8, 'autofocus': True}))

class FamilyForm(forms.ModelForm):
    name = forms.CharField(label='Как назовем семью?', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' Учиха клан', 'autofocus': True}))

    class Meta:
        model = FamilyMember
        exclude = ['user']
        fields = ('name',)