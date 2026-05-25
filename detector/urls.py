from django.urls import path
from . import views

urlpatterns = [
    path('', views.diagnostic_view, name='diagnostic_view'),
    path('api/predict/', views.api_predict_skin_disease, name='api_predict')
]