from django.db import models
from django import forms
from django.forms import ModelForm, Textarea, TextInput

from submit.models import Game, Developer
from transfer.spreadsheet import Spreadsheet

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = '__all__'
#        exclude = ['developer']
        widgets = {
            'notes' : Textarea(attrs={'cols':40,'rows':3}),
        }

    def clean_name(self):
        if Game.objects.filter(name__iexact = self.cleaned_data.get('name')).count() > 0:
            raise ValidationError('Duplicate game!')
        return self.cleaned_data.get('name')


class DeveloperForm(ModelForm):
    class Meta:
        model = Developer
        fields = '__all__'
        widgets = {
            'notes' : Textarea(attrs={'cols':40,'rows':3,'class':'dev'}),
            'name' : TextInput(attrs={'class': 'dev'}),
            'email' : TextInput(attrs={'class': 'dev'}),
            'twitter' : TextInput(attrs={'class': 'dev'}),
            'skype' : TextInput(attrs={'class': 'dev'}),
            'url' : TextInput(attrs={'class': 'dev'}),
            'mailing_address' : TextInput(attrs={'class': 'dev'}),






        }

    def clean_name(self):
        if Developer.objects.filter(name__iexact = self.cleaned_data.get('name')).count() > 0:
            raise ValidationError('Duplicate dev!')
        return self.cleaned_data.get('name')

