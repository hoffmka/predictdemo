from django import forms
import datetime

class THSSearchPsnByPatientForm(forms.Form):
    DOMAIN_CHOICES = (
        #('demo', 'Demo'),
        ('model_A', 'CML Model: Longtime response'),
        ('model_B', 'CML Model: Recurrance probability'),
        ('FB1', 'Haematology'),
    )
    #domain = forms.ChoiceField(widget = forms.Select(),
    #        choices = DOMAIN_CHOICES, initial = 'model_B', required = True, label = 'Model (Domain)')
    firstname = forms.CharField(max_length = 40, initial = 'Peter', required = True)
    lastname =  forms.CharField(max_length = 40, initial = 'Liebknecht', required = True)
    gender = forms.ChoiceField(widget = forms.Select(),
            choices = ([('F','Female'), ('M','Male'), ]), initial = 'M', required = True)
    birthplace = forms.CharField(max_length = 40, initial = 'Berlin', required = False)
    birthdate = forms.DateField(initial = datetime.datetime.strptime('1977-03-03', '%Y-%m-%d'), required = True)

# class ModelSelectionForm(forms.Form):
#     MODEL_CHOICES = (
#         ('',''),
#         ('model_a',u'Prediction of long-term response in continously TKI-treated CML'),
#         ('model_b',u'Recurrance prediction after half dose TKI treatment'),
#         ('model_c',u'Modell C'),
#     )
#     model = forms.ChoiceField(widget = forms.Select(), choices = MODEL_CHOICES)