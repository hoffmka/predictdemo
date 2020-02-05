from django import forms
import datetime

class THSSearchPsnByPatientForm(forms.Form):
    domain = forms.ChoiceField(widget = forms.Select(),
            choices = ([('demo','demo'), ]), initial = 'demo', required = True)
    firstname = forms.CharField(max_length = 40, initial = 'Lehmann')
    lastname =  forms.CharField(max_length = 40, initial = 'Adda')
    gender = forms.ChoiceField(widget = forms.Select(),
            choices = ([('F','Female'), ('M','Male'), ]), initial = 'F', required = True)
    birthplace = forms.CharField(max_length = 40, initial = 'Berlin', required = False)
    birthdate = forms.DateField(initial = datetime.datetime.strptime('1940-11-17', '%Y-%m-%d'), required = True)
