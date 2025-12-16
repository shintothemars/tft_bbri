from django.urls import path
from .views import PredictStockView, HealthCheckView

urlpatterns = [
    path('predict/', PredictStockView.as_view(), name='predict'),
    path('health/', HealthCheckView.as_view(), name='health'),
]
