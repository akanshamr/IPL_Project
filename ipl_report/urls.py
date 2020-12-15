
from django.urls import path

from ipl_report import views

app_name = 'ipl_report'
urlpatterns = [
    path('report/', views.report, name='report'),
]
