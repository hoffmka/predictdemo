from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from lazysignup.decorators import allow_lazy_user
from rolepermissions.checkers import has_role
from rolepermissions.roles import assign_role, remove_role

from .forms import SignUpForm

# Create your views here.

@allow_lazy_user
def lazysignup(request):
    """
    This view will create a temporary (guest) user account.
    The user is in the group "dept_haematology" and in the group "cml_trial"
    """
    cml_trial = Group.objects.get(id = 2) 
    cml_trial.user_set.add(request.user)
    return redirect('home')


def switch_lazyuser_group(request):
    """
    This view will switch the lazy user from group dept_haematology to trial_cml or the other way
    """

    if has_role(request.user, "trial_cml"):
        remove_role(request.user, "trial_cml")
        assign_role(request.user, "dept_haematology")
    elif has_role(request.user, "dept_haematology"):
        remove_role(request.user, "dept_haematology")
        assign_role(request.user, "trial_cml")
    else:
        assign_role(request.user, "dept_haematology")

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
    
def setGroup(request):
    dept_haematology = Group.objects.get(id = 1) 
    dept_haematology.user_set.add(request.user)
