from django.urls import path
from .views import UssdCallbackView

urlpatterns = [
    path("ussd/", UssdCallbackView.as_view(), name="ussd-callback"),
]
