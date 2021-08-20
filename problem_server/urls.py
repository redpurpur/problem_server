"""problem_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'', main_views.ProblemListView.as_view(), name='index_page'),
    path(r'problem/<int:pk>/', main_views.ProblemView.as_view(), name='problem_page'),

    path(r'api/submissions/',
         main_views.SubmissionListApiView.as_view(),
         name='submission_list',
    ),
    path(r'api/submissions/<int:pk>/',
         main_views.SubmissionDetailApiView.as_view(),
         name='problem_detail',
    ),
    path(r'api/problem/<int:problem_id>/send_submission/',
         main_views.ReceiveSubmissionApiView.as_view(),
         name='send_submission',
    ),
]
