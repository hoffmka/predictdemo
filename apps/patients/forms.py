from django import forms
import datetime

class THSSearchPsnByPatientForm(forms.Form):
    DOMAIN_CHOICES = (
        ('fb_haematology', 'Haematology'),
        ('fb_psychiatry', 'Psychiatry'),
    )
    #domain = forms.ChoiceField(widget = forms.Select(),
    #        choices = DOMAIN_CHOICES, initial = 'fb_haematology', required = True, label = 'Medical department (Domain)')
    firstname = forms.CharField(max_length = 40, required = True, initial = 'Max')
    lastname =  forms.CharField(max_length = 40, required = True, initial = 'Mustermann')
    gender = forms.ChoiceField(widget = forms.Select(),
            choices = ([('F','Female'), ('M','Male'), ]), required = True, initial = 'M')
    birthplace = forms.CharField(max_length = 40, required = False)
    birthdate = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2020)), required = True, initial = '2000-01-01')