from django import forms
from lighting.models import Zone

class ZoneForm(forms.ModelForm):
    name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'id':'name', 'class': 'form-control', 'readonly':'readonly'}))
    pir_enabled = forms.BooleanField(required=False, label='PIR enabled', widget=forms.CheckboxInput(attrs={'id':'pir_enabled', 'class':'form-control'})) 
    test_active = forms.BooleanField(required=False, label='Test active', widget=forms.CheckboxInput(attrs={'id':'test_active', 'class':'form-control'})) 
    on_delay = forms.IntegerField(min_value=0, max_value=100, label='On delay', widget=forms.NumberInput(attrs={'on_delay':'on_delay', 'class': 'form-control'})) 
                        
    class Meta:         
        model = Zone
        fields=("name", "pir_enabled", "test_active", "on_delay", )
        exclude = ("slug", )
        
