from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse,reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from rolepermissions.mixins import HasPermissionsMixin
from predictDemo.roles.mixins import HasObjectPermissionMixin

from .models import Trial, Document
from .forms import DocumentForm

# Create your views here.

class TrialListView(ListView):
    """
    This view will list the trials
    """
    #allowed_roles = 'consultant_admin'
    queryset = Trial.objects.order_by('name')
    context_object_name = 'trials_list'
    template_name = 'trials/trials_list.html'

class TrialCreateView(CreateView):
    """
    This view will create a trial
    """
    #allowed_roles = 'consultant_admin'
    model = Trial
    fields =('studyCode', 'name', 'description', 'clinicalTrials', 'eudraCT')
    template_name = 'trials/trials_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.createdBy = self.request.user
        obj.save()        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trials:trials_detail', kwargs={'trial_pk' : self.object.pk})

class TrialDeleteView(HasObjectPermissionMixin, DeleteView):
    """
    This view will delete the trial
    """
    checker_name = 'delete_trial'
    model= Trial
    template_name = 'trials/trials_delete.html'
    pk_url_kwarg = 'trial_pk'
    success_url = reverse_lazy('trials:trials_list')

class TrialDetailView(HasObjectPermissionMixin, DetailView):
    """
    This view will retrieve the details for a trial
    """
    checker_name = 'access_trial'
    model = Trial
    template_name = 'trials/trials_detail.html'
    pk_url_kwarg = 'trial_pk'


class TrialUpdateView(HasObjectPermissionMixin, UpdateView):
    """
    This view will update a trial
    """
    #allowed_roles = 'consultant_admin'
    checker_name = 'change_trial'
    model = Trial
    fields =('studyCode', 'name', 'description', 'clinicalTrials', 'eudraCT', 'disease')
    template_name = 'trials/trials_update.html'
    pk_url_kwarg = 'trial_pk'
    context_object_name = 'trial'

    def form_valid(self, form):
        trial = form.save(commit=False)
        trial.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trials:trials_detail', kwargs={'trial_pk' : self.object.pk})

class TrialUploadListView(HasObjectPermissionMixin, DetailView):
    """
    This view will list the documents for selected trial
    """
    checker_name = 'access_trial'
    model = Trial
    template_name = 'trials/trials_file_list.html'
    pk_url_kwarg = 'trial_pk'

def trials_file_upload(request, trial_pk):
    """
    This method will perform a file upload
    """
    trial = get_object_or_404(Trial, pk=trial_pk)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.trial = trial
            fs.uploaded_by = request.user
            fs.save()
            redirect_to = reverse('trials:trials_file_list', kwargs={'trial_pk': trial_pk})
            return redirect(redirect_to)
    else:
        form = DocumentForm()
    return render(request, 'trials/trials_file_upload.html', {
    #return render(request, 'trials/trials_detail.html', {
        'trial': trial,
        'form': form
    })

class TrialUploadDetailView(HasObjectPermissionMixin, DetailView):
    """
    This view will retrieve the details for a trial
    """
    checker_name = 'access_trial_upload'
    model = Document
    template_name = 'trials/trials_file_detail.html'
    pk_url_kwarg = 'document_pk'

class TrialUploadUpdateView(HasObjectPermissionMixin, UpdateView):
    """
    This view will update a document
    """
    checker_name = 'access_trial_upload'
    model = Document
    fields =('description',)
    template_name = 'trials/trials_file_update.html'
    pk_url_kwarg = 'document_pk'
    context_object_name = 'document'

    def get_success_url(self):
        return reverse_lazy('trials:trials_upload_detail', kwargs={'document_pk' : self.object.pk})

class TrialUploadDeleteView(HasObjectPermissionMixin, DeleteView):
    """
    This view will delete the trial
    """
    checker_name = 'access_trial_upload'
    model = Document
    template_name = 'trials/trials_file_delete.html'
    pk_url_kwarg = 'document_pk'

    def get_success_url(self):
        trial = self.object.trial
        return reverse_lazy('trials:trials_file_list', kwargs={'trial_pk': trial.pk})