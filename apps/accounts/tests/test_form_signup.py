from django.test import TestCase
from ..forms import SignUpForm

class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        '''
        The form must contain the fields 'username', 'email' and 2 password fields
        '''
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)