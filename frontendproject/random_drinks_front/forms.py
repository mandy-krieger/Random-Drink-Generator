from django import forms

class NameForm(forms.Form):

    ingred = forms.CharField(label='ingred', max_length=100)
