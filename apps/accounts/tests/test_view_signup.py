from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import resolve, reverse
from django.test import TestCase
from ..views import signup
from ..forms import SignUpForm

class SignUpTests(TestCase):

    def setUp(self):
        ''' 
        Setting response object 
        '''
        url = reverse('accounts:signup')
        self.response = self.client.get(url, follow=True)

    def test_signup_status_code(self):
        ''' 
        Testing the status code (success = 200) 
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        ''' 
        Testing if the url "/signup" is given the correct view function 
        '''
        view = resolve('/accounts/signup/')
        self.assertEquals(view.func, signup)

    def test_contains_form(self):
        ''' 
        Testing if there is a form 
        '''
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)

    def test_csrf(self):
        '''
        Testing if there is a response token 
        '''
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class SuccessfulSignupTests(TestCase):
    '''
    Testing a successful sign up
    '''
    def setUp(self):
        url = reverse('accounts:signup')
        data = {
            'username': 'john',
            'email': 'john@tu-dresden.de',
            'password1': 'Abcdefg123456',
            'password2': 'Abcdefg123456'
        }
        self.response = self.client.post(url, data)
        self.accounts_url = reverse('accounts:my_account')

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to the home page
        '''
        self.assertRedirects(self.response, self.accounts_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        '''
        Creat a new request to an arbitrary page.
        The resulting response should now have a 'user' to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.accounts_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.post(url, {}) # submit an empty dictionary

    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        '''
        An invalid form submission should return form errors
        '''
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        '''
        An invalid form submission should not create a user
        '''
        self.assertFalse(User.objects.exists())
