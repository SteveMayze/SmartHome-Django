from django import forms
from i2c.models import Device

class DeviceForm(forms.ModelForm):
    address = forms.IntegerField(label='Address',  widget=forms.TextInput(attrs={'id':'address', 'class': 'form-control', 'readonly':'readonly'})) # , help_text="Enter the value for the three bit device address")
    name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'id':'name', 'class': 'form-control'}))
    description = forms.CharField(max_length=200, label='Description', widget=forms.TextInput(attrs={'id':'description', 'class': 'form-control'})) #, help_text="Enter a description for the device")
 
    class Meta:
        model = Device
        fields=("address", "name", "description", )
        exclude = ('device_type', 'slug',)
        
        
        
