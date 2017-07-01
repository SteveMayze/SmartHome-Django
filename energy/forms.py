from django import forms
from energy.models import Resource, ResourceEntry

class ResourceGraphForm( forms.Form ):

	resources = Resource.objects.all()
	

	resource = forms.ModelChoiceField(label="Resource", queryset=resources, empty_label=None, initial=resources[0], widget=forms.Select(attrs={'class': 'form-control'}))
	start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))



class ResourceEntryForm( forms.ModelForm ):
	
	resources = Resource.objects.all()
	
	resource = forms.ModelChoiceField(label="Resource", queryset=resources, empty_label=None, initial=resources[0], widget=forms.Select(attrs={'class': 'form-control'}))
	time_stamp = forms.DateField( label="Date", widget=forms.TextInput(attrs={'class': 'form-control'}))
	value_close = forms.DecimalField( label="Reading", max_digits=9, decimal_places=4, widget=forms.TextInput(attrs={'class': 'form-control'}))
	value_adjust = forms.DecimalField( label="Adjustment", max_digits=9, decimal_places=4, initial=0.0, widget=forms.TextInput(attrs={'class': 'form-control'}))
	comment = forms.CharField(label="Comment", max_length=200, widget=forms.Textarea(attrs={'class': 'form-control'}))


	class Meta:
		model = ResourceEntry
		fields = ("resource", "time_stamp", "value_close", "value_adjust", "comment", )
