from django.urls import path, include

from sample import views

urlpatterns = [
    path('samples/', views.SamplesList.as_view()),
    path('samples/search', views.search),
    path('samples/<slug:sample_id>', views.SampleDetail.as_view()),
    path('patients/<slug:patient_id>', views.PatientDetail.as_view()),
]