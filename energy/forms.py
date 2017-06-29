from django import forms
from energy.models import Resource

class ResourceGraphForm( forms.Form ):

    resources = Resource.objects.all()
    
    resource = forms.ModelChoiceField(label="Resource", queryset=resources, widget=forms.Select(attrs={'class': 'form-control'}))
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))

