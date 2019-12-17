from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from lazysignup.decorators import allow_lazy_user

from .forms import SignUpForm

# Create your views here.

@allow_lazy_user
def lazysignup(request):
    """
    This view will create a temporary (guest) user account
    """
    return redirect('home')

def signup(request):
    """
    This view will create a user account
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend = 'django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:my_account')
    else:
        form = SignUpForm()
    return render(request,'accounts/signup.html', {'form':form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(SuccessMessageMixin, UpdateView):
    """
    This view will update the account information
    """
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'accounts/my_account.html'
    success_message = 'Your user account has been changed successfully!'
    success_url = reverse_lazy('accounts:my_account')

    def get_object(self):
        return self.request.user
    
