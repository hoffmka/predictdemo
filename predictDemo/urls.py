"""predictDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import TemplateView

# Load plotly apps -this triggers their registration
import plotlydash.DashExampleApp

from django_plotly_dash.views import add_to_session


from apps.dashtest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('convert/', include('lazysignup.urls')), #convert lazy accounts to real accounts
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('dash/', views.dashtest, name='dash'),
    path('patients/', include('apps.patients.urls', namespace='patients')),
    path('trials/', include('apps.trials.urls', namespace='trials')),
    path('views/', include('apps.dbviews.urls', namespace='dbviews')),
    path('destiny/', include('apps.udv_destiny.urls', namespace='udv_destiny')),
    path('docs/', include('docs.urls')), # third party include
    path('shiny/', include('apps.shiny.urls')),

    # django_plotly_dash app
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]

if settings.DEBUG: # for serving media files locally
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)