from django import forms
from .models import Character

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': '', 'placeholder': '입력'}),
        }
