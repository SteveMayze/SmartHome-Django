from django import forms
from lighting.models import Zone

class ZoneForm(forms.ModelForm):
    name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}))
    pir_enabled = forms.BooleanField(required=False, label='PIR enabled') 
    test_active = forms.BooleanField(required=False, label='Test active') 
    on_delay = forms.IntegerField(min_value=0, max_value=100, label='On delay', widget=forms.NumberInput(attrs={'class': 'form-control'})) 
                        
    class Meta:         
        model = Zone
        fields=("name", "pir_enabled", "test_active", "on_delay", )
        exclude = ("slug", )
        
