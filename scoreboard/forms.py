from django import forms

class HomeForm(forms.Form):
    text = forms.CharField(required = False, label = '', widget = forms.TextInput(attrs = {'placeholder':' Enter Twitter Handle'}))